from config import DB
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType
from models import StorageGroup, Object
from datetime import datetime
import requests

session = Session(DB.IoT_ip, DB.IoT_port, DB.IoT_username, DB.IoT_password)

def init_db():
    session.open(False)
    response = requests.get(DB.MySQL_API_URL+'/objects/')
    if response.status_code == 200:
        obj = response.json()['data']

        saguenay = StorageGroup("root.sg_saguenay")
        saguenay.add_to_db(session)

        for o in obj:
            if o['status_reg'] != 0:
                new = Object(o['nom'], o['type_obj'])
                new.add_to_db(session)

                for x in range(2):
                    d = datetime.now()
                    data = [True]
                    if o['type_obj'] == 'Camera':
                        data.append(new.nom+"_photo_"+str(d.strftime("%m/%d/%Y-%H:%M:%S"))+".jpg")
                    elif o['type_obj'] == 'Sonde_Niveau_Eau':
                        data.append(str(d.microsecond%50))
                        data.append(float(d.microsecond%38.3))
                    else:
                        data.append(new.nom+"_mesure_"+str(x))

                    new.add_data(session, data)
    
    session.close()