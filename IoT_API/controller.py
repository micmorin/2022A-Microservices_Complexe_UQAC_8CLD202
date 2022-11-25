import requests
from models import StorageGroup, Object, Analytics
from database_init import session, init_db
from flask import jsonify, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from config import DB
import json, re
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor

########
# MAIN #
########

def main_register():
    data = request.get_json()
    response = requests.post( DB.MySQL_API_URL+'/objects/create', 
        data=json.dumps( {"type":data['type']}), 
        headers={'Content-Type': 'application/json'})

    # Register Reussie    
    if response.status_code == 200:
        
        return jsonify({'data':response.json()['data']}), 200
    
    # Register Echoue
    else:
        return jsonify({'data':response.json()['message']}), response.status_code

def main_confirm():
    data = request.get_json()
    try :
        session.open(False)
        obj = Object(data['nom'], data['type_obj'])
        obj.add_to_db(session)
        session.close()
    except :
        pass
    return jsonify(), 200
    

def main_test():
    session.open(False)
    resultats = Analytics(session)
    session.close()
    return jsonify({"data":resultats.mysql_metrics}),200

def main_init():
    if DB.need_init:
        init_db()
        DB.need_init = False
    return jsonify(),200

def main_analytics():
    session.open(False)
    resultats = Analytics(session)
    session.close()
    return jsonify({
        "iotdb_records":resultats.iotdb_records,
        "iotdb_metrics":resultats.iotdb_metrics,
        "mysql_records":resultats.mysql_records,
        "mysql_metrics":resultats.mysql_metrics,
        "summary":resultats.summary
        }),200


########
# DATA #
########

def data_create():
    data = request.get_json()
    if data['status'] == '0':
        return jsonify({'message':'Objet non confirmé'}), 503
    elif data['status'] == '2':
        return jsonify({'message':'Objet désactivé'}), 503
    try :
        session.open(False)
        obj = Object(data['nom'], data['type'])
        obj.add_data(session, data['measures'])
        session.close()
        return jsonify({'message':'SUCCESS - Added data '+ ' '.join(str(e)+' ' for e in data['measures']) +' for '+data['nom']}), 200
    except Exception as e:
        session.close()
        return jsonify({'message':'FAILURE - Unable to add data '+ ' '.join(str(e)+' ' for e in data['measures']) +' for '+data['nom']}), 500

def data_delete(): 
    data = request.get_json()
    try :
        session.open(False)
        obj = Object(data['nom'], data['type'])
        obj.delete_data(session, data['time'])
        session.close()
        return jsonify({'message':'SUCCESS - Deleted data for '+data['nom']+' at '+data['time']}), 200
    except Exception as e:
        session.close()
        return jsonify({'message':'FAILURE - Unable to delete data for '+data['nom']+' at '+data['time']}), 500