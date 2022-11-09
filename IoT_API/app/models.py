import array, requests, re
from queue import Empty
from datetime import datetime, timedelta
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from config import DB

class StorageGroup():

    def __init__(self, nom:str):
        self.nom = nom


    def add_to_db(self, session:Session):
        session.set_storage_group(self.nom)

    def __repr__(self):
        return self.nom

class Object():

    def __init__(self, nom:str, type:str="other", storage_group:str="root.saguenay"):
        self.storage_group = storage_group
        self.nom = nom.replace(" ", "_")
        self.type = type
        self.fields = []
        self.field_types = []
        self.encodings = []
        self.compressors = []
        self.add_field("IO",TSDataType.BOOLEAN)
        if type == 'Camera':
            self.add_field("Photo",TSDataType.TEXT)
        elif type == 'Sonde_Niveau_Eau':
            self.add_field("Water_Level",TSDataType.INT64)
            self.add_field("Water_Temperature",TSDataType.FLOAT)
        else:
            self.add_field("Mesure",TSDataType.TEXT)

    def add_field(self, field:str, field_type:TSDataType): 
        self.fields.append(field)
        self.field_types.append(field_type)
        self.encodings.append(TSEncoding.PLAIN)
        self.compressors.append(Compressor.SNAPPY)

    def add_to_db(self, session:Session):
        if not session.check_time_series_exists(self) and self.fields is not Empty:
            session.create_aligned_time_series(
                self.__repr__(),
                self.fields,
                self.field_types,
                self.encodings ,
                self.compressors
            )

    def add_data(self, session:Session, data:array):
        if not session.check_time_series_exists(self):
            sql = 'insert into '+self.__repr__()+'('
            for x in range(len(self.fields)):
                sql = sql + self.fields[x]
                if x < len(self.fields)-1:
                    sql = sql + ','
                else:
                    sql = sql + ') aligned values('

            for x in range(len(data)):
                if self.field_types[x] == TSDataType.TEXT:
                    sql = sql + "'" + str(data[x]) + "'" 
                else:
                    sql = sql +  str(data[x]) 
                if x < len(data)-1:
                    sql = sql + ','
                else:
                    sql = sql + ')'

            session.execute_non_query_statement(sql)

    def delete_data(self, session:Session, time:str):
        if not session.check_time_series_exists(self):
            t_start = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")+timedelta(hours=5)
            t_end = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")+timedelta(hours=5,seconds=1)
            sql = 'delete from '+self.__repr__()+'.* where time >=' + t_start.strftime("%Y-%m-%d %H:%M:%S") + ' and time <=' + t_end.strftime("%Y-%m-%d %H:%M:%S") + ';'
            session.execute_non_query_statement(sql)

    def select_all(self, session:Session):
        data = session.execute_query_statement("select * from "+self.__repr__()).todf().to_dict(orient='records')
        for x in range(len(data)):
            t = datetime.fromtimestamp(data[x]["Time"] / 1e3)-timedelta(hours=5)
            data[x]["Time"] = t.strftime("%Y-%m-%d %H:%M:%S")
            for f in range(len(self.fields)):
                if self.field_types[f] == TSDataType.FLOAT:
                    data[x][str(f)] = round(data[x][self.__repr__()+"."+self.fields[f]],2)
                else:
                    data[x][str(f)] = data[x][self.__repr__()+"."+self.fields[f]]
                del data[x][self.__repr__()+"."+self.fields[f]]  
        return data

    def __repr__(self):
        return self.storage_group+'.'+self.nom

    def to_json(self):
        return {
            "sg": self.storage_group,
            "nom":self.nom,
            "fields":self.fields,
            "FT":self.field_types
        }

class Analytics():
    def __init__(self, session:Session):
        self.session = session
        self.summary = []      # init + Display
        self.iotdb_records = []
        self.iotdb_metrics = []
        self.mysql_records = requests.get(DB.MySQL_API_URL+'/objects').json()['data']
        self.mysql_metrics = requests.get(DB.MySQL_API_URL+'/metrics').json()['data']
        self.init_records()
        self.init_metrics()
        self.init_summary()


    def init_records(self): 
        # RECORDS INIT
        for o in requests.get(DB.MySQL_API_URL+'/objects/').json()['data']:
            if o['status_reg'] != 0:
                current = Object(o['nom'], o['type_obj'])
                self.iotdb_records.append({
                    "nom": o['nom'].replace("_", " "),
                    "type":current.type, 
                    "mesures":current.fields, 
                    "records":current.select_all(self.session)
                    })

    def init_metrics(self): 
        # METRICS INIT
        # Server Response to legible array
        array = []
        prev=""
        current = ""
        for char in str(requests.get('http://'+DB.IoT_ip+':9091/metrics').content):
            if char == "\\":
                array.append(current)
                current = ""
            elif (char == "n" and prev == "\\") or prev =="" or (char == "\'" and prev == "b"): pass
            else:
                current= current + char
            prev = char

        # Legible array to Metrics dict
        for item in array:
            if re.search("^# HELP", item) or re.search("^# TYPE", item): pass
            else:
                x = re.split("{|}\s", item)
                if len(x) == 3:
                    d = re.split("\"", x[1])
                    fin = ""
                    for i in range(len(d)):
                        if i % 2 == 0: pass
                        else:
                            fin = fin + d[i]
                            if i < len(d)-2:
                                fin = fin + ' - '

                    self.iotdb_metrics.append({
                        "title":x[0],
                        "description":fin,
                        "measure":x[2]
                        })

    def init_summary(self):
        self.summary.append({"title":"Donnees de IoTDB", "data": []})
        self.summary.append({"title":"Metrics de IoTDB", "data": []})
        self.summary.append({"title":"Donnees de MySQL", "data": []})
        self.summary.append({"title":"Metrics de MySQL", "data": []})

        self.init_summary_iot_records()
        self.init_summary_iot_metrics()
        self.init_summary_mysql_records()
        self.init_summary_mysql_metrics()

        

    def init_summary_iot_records(self):
        entrees_total = 0
        photos_total = 0
        photos_devices = 0
        sonde_devices = 0
        niv_eau_total = 0
        niv_eau_dev = 0
        temp_eau_total = 0
        temp_eau_dev = 0
        total_temps = timedelta()
        total_ON = timedelta()
        for obj in self.iotdb_records:
            entrees_total = entrees_total + len(obj['records'])
            total_temps = total_temps + (datetime.strptime(obj['records'][len(obj['records'])-1]['Time'],'%Y-%m-%d %H:%M:%S') - datetime.strptime(obj['records'][0]['Time'],'%Y-%m-%d %H:%M:%S'))
            
            if obj['type'] == 'Camera':
                photos_devices = photos_devices + 1

                dev_ON_total = timedelta()
                dev_ON_prev_bool = False
                dev_ON_pre_time = datetime(1970,1,1)

                for record in obj['records']: 
                    if record["1"] != " ": photos_total = photos_total +1

                    if dev_ON_pre_time != datetime(1970,1,1):
                        if dev_ON_prev_bool: dev_ON_total = dev_ON_total + (dev_ON_pre_time-datetime.strptime(record['Time'],'%Y-%m-%d %H:%M:%S'))
                    dev_ON_pre_time = datetime.strptime(record['Time'],'%Y-%m-%d %H:%M:%S')
                    dev_ON_prev_bool = record['0']

                total_ON = total_ON + dev_ON_total


            elif obj['type'] == 'Sonde_Niveau_Eau':
                sonde_devices = sonde_devices + 1
                
                dev_ON_total = timedelta()
                dev_ON_prev_bool = False
                dev_ON_pre_time = datetime(1970,1,1)

                for record in obj['records']: 
                    if record["1"] != " ": 
                        niv_eau_dev = niv_eau_dev +1
                        niv_eau_total = niv_eau_total + record["1"]
                    if record["2"] != " ": 
                        temp_eau_dev = temp_eau_dev +1
                        temp_eau_total = temp_eau_total + record["2"]

                    if dev_ON_pre_time != datetime(1970,1,1):
                        if dev_ON_prev_bool: dev_ON_total = dev_ON_total + (dev_ON_pre_time-datetime.strptime(record['Time'],'%Y-%m-%d %H:%M:%S'))
                    dev_ON_pre_time = datetime.strptime(record['Time'],'%Y-%m-%d %H:%M:%S')
                    dev_ON_prev_bool = record['0']
                
                total_ON = total_ON + dev_ON_total

            else:
                dev_ON_total = timedelta()
                dev_ON_prev_bool = False
                dev_ON_pre_time = datetime(1970,1,1)

                for record in obj['records']:
                    if dev_ON_pre_time != datetime(1970,1,1):
                        if dev_ON_prev_bool: dev_ON_total = dev_ON_total + (dev_ON_pre_time-datetime.strptime(record['Time'],'%Y-%m-%d %H:%M:%S'))
                    dev_ON_pre_time = datetime.strptime(record['Time'],'%Y-%m-%d %H:%M:%S')
                    dev_ON_prev_bool = record['0']

                total_ON = total_ON + dev_ON_total


        self.summary[0]['data'].append({"title":"Entrees Totales","data":entrees_total})
        self.summary[0]['data'].append({"title":"Entrees en Moyenne","data":entrees_total/len(self.iotdb_records)})
        self.summary[0]['data'].append({"title":"Photos Totales","data":photos_total})
        self.summary[0]['data'].append({"title":"Photos en Moyenne","data":photos_total/photos_devices})
        self.summary[0]['data'].append({"title":"Niveau Eau Moyen","data":niv_eau_total/niv_eau_dev})
        self.summary[0]['data'].append({"title":"Temperature Eau Moyen","data":temp_eau_total/temp_eau_dev})
        self.summary[0]['data'].append({"title":"Pourcentage ON Moyen","data":str(-total_ON/total_temps*100)+'%'})

    def init_summary_iot_metrics(self):
        for obj in self.iotdb_metrics:
            if obj['description'] == 'timeSeries - normal':
                self.summary[1]['data'].append({"title":"Different types de donnees","data":obj['measure']})
            if obj['title'] == 'operation_histogram_sum':
                self.summary[1]['data'].append({"title":"Requete faites","data":obj['measure']})
            if obj['title'] == 'entry_seconds_count' and obj['description'] == 'fetchResults':
                self.summary[1]['data'].append({"title":"Temps total pour les requetes","data":obj['measure']})
            if obj['description'] == 'storageGroup_root.saguenay':
                self.summary[1]['data'].append({"title":"Memoire utilisee","data":obj['measure']})

    def init_summary_mysql_records(self):
        total_letters_in_names = 0
        total_letters_in_tokens = 0
        total_new = 0
        total_types = []
        for obj in self.mysql_records:
            total_letters_in_names = total_letters_in_names + len(obj['nom'])
            total_letters_in_tokens = total_letters_in_tokens + len(obj['token'])
            if obj['status_reg'] == 0: total_new = total_new + 1
            if obj['type_obj'] not in total_types: total_types.append(obj['type_obj'])
        


        self.summary[2]['data'].append({"title":"Total d'objets connectes","data":len(self.mysql_records)})
        self.summary[2]['data'].append({"title":"Longueur moyenne des noms","data":total_letters_in_names/len(self.mysql_records)})
        self.summary[2]['data'].append({"title":"Longueur moyenne des tokens","data":total_letters_in_tokens/len(self.mysql_records)})
        self.summary[2]['data'].append({"title":"Moyenne d'objet par type","data":len(self.mysql_records)/len(total_types)})
                
    def init_summary_mysql_metrics(self):

        short = 1000000
        long = 0
        total = 0
        list = []
        for obj in self.mysql_metrics:
            if obj['access_duration'] < short: short = obj['access_duration']
            if obj['access_duration'] > long: long = obj['access_duration']
            total = total + obj['access_duration']
            list.append(obj['access_page'])

        self.summary[3]['data'].append({"title":"Plus longue demande (microSec)","data":long})
        self.summary[3]['data'].append({"title":"Plus courte demande (microSec)","data":short})
        self.summary[3]['data'].append({"title":"Temps de demande moyen","data":total/len(self.mysql_metrics)})
        self.summary[3]['data'].append({"title":"Page la plus demande","data":mostFrequent(list, len(list))})


# (c) https://www.geeksforgeeks.org/frequent-element-array/
def mostFrequent(arr, n):
 
    # Sort the array
    arr.sort()
 
    # find the max frequency using
    # linear traversal
    max_count = 1
    res = arr[0]
    curr_count = 1
 
    for i in range(1, n):
        if (arr[i] == arr[i - 1]):
            curr_count += 1
        else:
            curr_count = 1
 
         # If last element is most frequent
        if (curr_count > max_count):
            max_count = curr_count
            res = arr[i - 1]
 
    return res