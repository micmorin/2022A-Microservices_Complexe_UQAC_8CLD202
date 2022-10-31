from queue import Empty
from sqlalchemy.orm import Session
from fastapi import status
from models import User, Profil, Calcul
from werkzeug.security import check_password_hash, generate_password_hash


def get_staff(db: Session):
    return db.query(Staff).all()

def add_staff(db: Session, ID:str, name: str, compet: str, ed: str, exp: str):
     db.query(Staff).add_entity(Staff(ID=ID, StaffName=name, Education=ed, Skills=compet, Experience=exp))
     db.commit()
     return db.query(Staff).all()

def mod_staff(db: Session, ID:str, name: str, compet: str, ed: str, exp: str):
     db.query(Staff).filter(Staff.ID == ID).update({'StaffName':name, 'Education':ed, 'Skills':compet, 'Experience':exp})
     db.commit()
     return db.query(Staff).all()

def del_staff(db: Session, ID:str):
     db.query(Staff).filter(Staff.ID == ID).delete()
     db.commit()
     return db.query(Staff).all()

########
# MAIN #
########

def main_index(db, response, request):
    return {"message":"Veuillez consulter la documentation de l'API"}

def main_login(db, response, request):
    data = request.json()
    u = db.query(User).filter(username=data["username"]).first()
    if check_password_hash(u.password, data["password"]):
        return {"message":"Connexion reussie", "data": u.to_json()}
    else:
          response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
          return {"message":"Identifiants invalides"}

########
# User #
########

def user_index(db, response, request):
    users = db.query(User).all()
    if users is Empty:
          response.status_code = status.HTTP_404_NOT_FOUND
          return {"message":"no user found"}
    else:
        users_obj = []
        for u in users:
            users_obj.append(u.to_json())
        return {"message":"ok", "data": users_obj}

def user_create(db, response, request):
    data = request.json()
    try:
        new_user = User(
            name=data['name'], 
            username=data['username'], 
            email=data['email'],
            password=data['password'],
            token=generate_password_hash(data['name']),
            profil_id="2"
            )
        db.query(User).add_entity(new_user)
        db.commit()
        return {"message":'Utilisateur enregistre!', "token": new_user.token, "id":new_user.id}
    except:
          response.status_code = status.HTTP_400_BAD_REQUEST
          return {"message":'Un probleme est survenu. Le nom d\'utilisateur existe peut etre deja. '}

def user_update(db, response, request):
    data = request.json()
    try:
        user = db.query(User).filter(id=data["id"]).update({
        'name': data['name'],
        'username': data['username'],
        'email': data['email']
        })
        db.commit()
        return {"message":"L'utilisateur " + user.username + " a ete mis a jour"}
    except:
          response.status_code = status.HTTP_400_BAD_REQUEST
          return {"message":'Un probleme est survenu.'}  

def user_delete(db, response, request):
    data = request.json()
    try:
        user = db.query(User).filter(id=data["id"]).first()
        db.session.delete(user)
        db.commit()
        return {"message":"L'utilisateur a ete supprime!"}
    except:
          response.status_code = status.HTTP_400_BAD_REQUEST
          return {"message":'Un probleme est survenu.'}    

##########
# Profil #
##########

def profil_index(db, response, request):
    profils = db.query(Profil).all()
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
        new_profil = Profil(
            description=data['description'], 
            )
        db.query(Profil).add_entity(new_profil)
        db.commit()
        return {"message":'Profil enregistre!'}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu. Le profil existe peut etre deja. '}

def profil_update(db, response, request):
    data = request.json()
    try:
        profil = db.query(Profil).filter(id=data["id"]).first()
        profil.description = data['description']
        db.commit()
        return {"message":"Le profil a ete mis a jour"}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu.'}    

def profil_delete(db, response, request):
    data = request.json()
    try:
        profil = db.query(Profil).filter(id=data["id"]).first()
        db.session.delete(profil)
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
    calculs = db.query(Calcul).filter(user_id=data["user_id"]).all()
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
        calcul = db.query(Calcul).filter(id=data["id"]).first()
        if calcul.user_id == data["user_id"]:
            db.session.delete(calcul)
            db.commit()
            return {"message":"Le profil a ete supprime!"}
        else:
             response.status_code = status.HTTP_501_NOT_IMPLEMENTED
             return {"message":'Acces Interdit.'} 
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":'Un probleme est survenu.'}  