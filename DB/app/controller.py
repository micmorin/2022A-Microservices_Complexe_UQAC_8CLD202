from queue import Empty
from models import User, Profil, Calcul
from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from database_init import db

########
# MAIN #
########

def main_index():
    return jsonify({"message":"Veuillez consulter la documentation de l'API"}), 404

def main_login():
    data = request.get_json()
    u = User.query.filter_by(username=data["username"]).first()
    if check_password_hash(u.password, data["password"]):
        return jsonify({"message":"Connexion reussie", "data": u.to_json()}), 200
    else:
        return jsonify({"message":"Identifiants invalides"}), 503

########
# User #
########

def user_index():
    users = User.query.all()
    if users is Empty:
        return jsonify({"message":"no user found"}), 404
    else:
        users_obj = []
        for u in users:
            users_obj.append(u.to_json())
        return jsonify({"message":"ok", "data": users_obj}), 200

def user_create():
    data = request.get_json()
    try:
        new_user = User(
            name=data['name'], 
            username=data['username'], 
            email=data['email'],
            password=data['password'],
            token=generate_password_hash(data['name']),
            profil_id="2"
            )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":'Utilisateur enregistre!', "token": new_user.token, "id":new_user.id}), 200
    except:
        return jsonify({"message":'Un probleme est survenu. Le nom d\'utilisateur existe peut etre deja. '}), 400

def user_update():
    data = request.get_json()
    try:
        user = User.query.filter_by(id=data["id"]).first()
        user.name = data['name']
        user.username = data['username']
        user.email = data['email']
        if data["password"] != "?":
            user.password = data['password']
        #user.profil_id =data['profilID']
        db.session.commit()
        return jsonify({"message":"L'utilisateur " + user.username + " a ete mis a jour"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

def user_delete():
    data = request.get_json()
    try:
        user = User.query.filter_by(id=data["id"]).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"L'utilisateur a ete supprime!"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

##########
# Profil #
##########

def profil_index():
    profils = Profil.query.all()
    if profils is Empty:
        return jsonify({"message":"no profil found"}), 404
    else:
        profils_obj = []
        for p in profils:
            profils_obj.append(p.to_json())
        return jsonify({"message":"ok", "data": profils_obj}), 200

def profil_create():
    data = request.get_json()
    try:
        new_profil = Profil(
            description=data['description'], 
            )
        db.session.add(new_profil)
        db.session.commit()
        return jsonify({"message":'Profil enregistre!'}), 200
    except:
        return jsonify({"message":'Un probleme est survenu. Le profil existe peut etre deja. '}), 400

def profil_update():
    data = request.get_json()
    try:
        profil = Profil.query.filter_by(id=data["id"]).first()
        profil.description = data['description']
        db.session.commit()
        return jsonify({"message":"Le profil a ete mis a jour"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

def profil_delete():
    data = request.get_json()
    try:
        profil = Profil.query.filter_by(id=data["id"]).first()
        db.session.delete(profil)
        db.session.commit()
        return jsonify({"message":"Le profil a ete supprime!"}), 200
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400     

##########
# CALCUL #
##########

def calcul_index():
    data = request.get_json()
    calculs = Calcul.query.filter_by(user_id=data["user_id"]).all()
    if calculs is Empty:
        return jsonify({"message":"no calculs found"}), 404
    else:
        calculs_obj = []
        for c in calculs:
            calculs_obj.append(c.to_json())
        return jsonify({"message":"ok", "data": calculs_obj}), 200

def calcul_delete():
    data = request.get_json()
    try:
        calcul = Calcul.query.filter_by(id=data["id"]).first()
        if calcul.user_id == data["user_id"]:
            db.session.delete(calcul)
            db.session.commit()
            return jsonify({"message":"Le profil a ete supprime!"}), 200
        else:
           return jsonify({"message":'Acces Interdit.'}), 501  
    except:
        return jsonify({"message":'Un probleme est survenu.'}), 400   