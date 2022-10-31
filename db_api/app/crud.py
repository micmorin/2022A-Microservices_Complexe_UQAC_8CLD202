from queue import Empty
from sqlalchemy.orm import Session
from fastapi import status
from . import models
from werkzeug.security import check_password_hash, generate_password_hash

########
# MAIN #
########

def main_index(db, response, request):
    return {"message":"Veuillez consulter la documentation de l'API"}

def main_login(db, response, request):
    data = request.json()
    u = db.query(models.Users).filter(username=data["username"]).first()
    if check_password_hash(u.password, data["password"]):
        return {"message":"Connexion reussie", "data": u.to_json()}
    else:
          response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
          return {"message":"Identifiants invalides"}

########
# User #
########

def user_index(db, response, request):
    users = db.query(models.Users).all()
    if users is Empty:
          response.status_code = status.HTTP_404_NOT_FOUND
          return {"message":"no user found"}
    else:
        return {"message":"ok", "data": users}

def user_create(db, response, request):
    data = request.json()
    try:
        new_user = models.Users(
            name=data['name'], 
            username=data['username'], 
            email=data['email'],
            password=data['password'],
            token=generate_password_hash(data['name']),
            profil_id="2"
            )
        db.query(models.Users).add_entity(new_user)
        db.commit()
        return {"message":'Utilisateur enregistre!', "token": new_user.token, "id":new_user.id}
    except:
          response.status_code = status.HTTP_400_BAD_REQUEST
          return {"message":'Un probleme est survenu. Le nom d\'utilisateur existe peut etre deja. '}

def user_update(db, response, request):
    data = request.json()
    try:
        db.query(models.Users).filter(id=data["id"]).update({
        'name': data['name'],
        'username': data['username'],
        'email': data['email']
        })
        db.commit()
        return {"message":"L'utilisateur a ete mis a jour"}
    except:
          response.status_code = status.HTTP_400_BAD_REQUEST
          return {"message":'Un probleme est survenu.'}  

def user_delete(db, response, request):
    data = request.json()
    try:
        db.query(models.Users).filter(id=data["id"]).delete()
        db.commit()
        return {"message":"L'utilisateur a ete supprime!"}
    except:
          response.status_code = status.HTTP_400_BAD_REQUEST
          return {"message":'Un probleme est survenu.'}    

##########
# Profil #
##########

def profil_index(db, response, request):
    profils = db.query(models.Profil).all()
    if profils is Empty:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":"no profil found"}
    else:
        profils_obj = []
        for p in profils:
            profils_obj.append(p.to_json())
        return {"message":"ok", "data": profils_obj}

def profil_create(db, response, request):
    data = request.json()
    try:
        new_profil = models.Profil(
            description=data['description'], 
            )
        db.query(models.Profil).add_entity(new_profil)
        db.commit()
        return {"message":'Profil enregistre!'}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu. Le profil existe peut etre deja. '}

def profil_update(db, response, request):
    data = request.json()
    try:
        profil = db.query(models.Profil).filter(id=data["id"]).first()
        db.query(models.Profil).filter(id=data["id"]).update({
        'description': data['description']
        })
        db.commit()
        return {"message":"Le profil a ete mis a jour"}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu.'}    

def profil_delete(db, response, request):
    data = request.json()
    try:
        db.query(models.Profil).filter(id=data["id"]).delete()
        db.commit()
        return {"message":"Le profil a ete supprime!"}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu.'}

##########
# CALCUL #
##########

def calcul_index(db, response, request):
    data = request.json()
    calculs = db.query(models.Calcul).filter(user_id=data["user_id"]).all()
    if calculs is Empty:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":"no calculs found"}
    else:
        calculs_obj = []
        for c in calculs:
            calculs_obj.append(c.to_json())
        return {"message":"ok", "data": calculs_obj}

def calcul_delete(db, response, request):
    data = request.json()
    try:
        calcul = db.query(models.Calcul).filter(id=data["id"]).first()
        if calcul.user_id == data["user_id"]:
            db.query(models.Calcul).filter(id=data["id"]).delete()
            db.commit()
            return {"message":"Le profil a ete supprime!"}
        else:
             response.status_code = status.HTTP_501_NOT_IMPLEMENTED
             return {"message":'Acces Interdit.'} 
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu.'}  