from queue import Empty
from models import User, Profil, Object
from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from database_init import SessionLocal
from datetime import datetime

########
# MAIN #
########

def main_index():
    return jsonify({"message":"Veuillez consulter la documentation de l'API"}), 404

def main_login():
    with SessionLocal.begin() as db:
        data = request.get_json()
        u = db.query(User).filter_by(username=data["username"]).first()
        if check_password_hash(u.password, data["password"]):
            return jsonify({"message":"Connexion reussie", "data": u.to_json()}), 200
        else:
            return jsonify({"message":"Identifiants invalides"}), 503

########
# User #
########

def user_index():
    with SessionLocal.begin() as db:
        users = db.query(User).all()
        if users is Empty:
            return jsonify({"message":"no user found"}), 404
        else:
            users_obj = []
            for u in users:
                users_obj.append(u.to_json())
            return jsonify({"message":"ok", "data": users_obj}), 200

def user_create():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            new_user = User(
                name=data['name'], 
                username=data['username'], 
                email=data['email'],
                password=data['password'],
                token=generate_password_hash(data['name']),
                profil_id="2"
                )
            db.add(new_user)
            return jsonify({"message":'Utilisateur enregistre!', "token": new_user.token, "id":new_user.id}), 200
    except:
            return jsonify({"message":'Un probleme est survenu. Le nom d\'utilisateur existe peut etre deja. '}), 400

def user_update():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            user = db.query(User).filter_by(id=data["id"]).first()
            user.name = data['name']
            user.username = data['username']
            user.email = data['email']
            if data["password"] != "?":
                user.password = data['password']
            #user.profil_id =data['profilID']
            return jsonify({"message":"L'utilisateur " + user.username + " a ete mis a jour"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

def user_delete():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            user = db.query(User).filter_by(id=data["id"]).first()
            db.delete(user)
            return jsonify({"message":"L'utilisateur a ete supprime!"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

##########
# Profil #
##########

def profil_index():
    with SessionLocal.begin() as db:
        profils = db.query(Profil).all()
        if profils is Empty:
            return jsonify({"message":"no profil found"}), 404
        else:
            profils_obj = []
            for p in profils:
                profils_obj.append(p.to_json())
            return jsonify({"message":"ok", "data": profils_obj}), 200

def profil_create():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            new_profil = Profil(
                description=data['description'], 
                )
            db.add(new_profil)
            return jsonify({"message":'Profil enregistre!'}), 200
    except:
        return jsonify({"message":'Un probleme est survenu. Le profil existe peut etre deja. '}), 400

def profil_update():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            profil = db.query(Profil).filter_by(id=data["id"]).first()
            profil.description = data['description']
            return jsonify({"message":"Le profil a ete mis a jour"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

def profil_delete():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            profil = db.query(Profil).filter_by(id=data["id"]).first()
            db.delete(profil)
            return jsonify({"message":"Le profil a ete supprime!"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

##########
# Object #
##########

def object_index():
    with SessionLocal.begin() as db:
        objets = db.query(Object).order_by(Object.status_reg).order_by(Object.nom).all()
        if objets is Empty:
            return jsonify({"message":"no objets found"}), 404
        else:
            objets_obj = []
            for o in objets:
                objets_obj.append(o.to_json())
            return jsonify({"message":"ok", "data": objets_obj}), 200

def object_create():           
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            new_object = Object(
                nom = data['type'],
                token = generate_password_hash(data['type']),
                type_obj = data['type'],
                date_reg = datetime.now(),
                status_reg = 0 
                )
            db.add(new_object)
            return jsonify({"message":'Objet ajoute!', 'data':new_object.to_json()}), 200
    except Exception as e:
        return jsonify({"message": e }), 400   

def object_update():
    try:
        with SessionLocal.begin() as db:
            data = request.get_json()
            profil = db.query(Object).filter_by(id=data["id"]).first()
            profil.nom = data['nom']
            profil.status_reg = data['status']
            return jsonify({"message":"Le profil a ete mis a jour"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400   