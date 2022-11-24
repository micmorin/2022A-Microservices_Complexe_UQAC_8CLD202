from database_init import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, TIMESTAMP, FetchedValue
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    username = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    token = Column(String(120), nullable=False)
    profil_id = Column(Integer, ForeignKey('profil.id'), nullable=False, default=2)

    profil = relationship("Profil")

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)    

    def to_json(self):
        return {"id":self.id,
                "name":self.name,
                "username":self.username,
                "email":self.email,
                "profil":self.profil.description,
                "token":self.token}

class Profil (Base):
    __tablename__ = "profil"

    id = Column(Integer, primary_key=True)
    description = Column(String(120), nullable=False)

    def __repr__(self):
        return '<Profil %r>' % self.description

    def to_json(self):
        return {"id":self.id,
                "description":self.description}

class Object (Base):
    __tablename__ = "objet_registration"

    id = Column(Integer, primary_key=True)
    nom = Column(String(120), unique=True, nullable=False)
    token = Column(String(120), unique=True, nullable=False)
    type_obj = Column(String(120), nullable=False)
    date_reg = Column(Date(), nullable=False)
    status_reg = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Objet %r>' % self.type_obj

    def to_json(self):
        return {"id":self.id,
                "nom":self.nom,
                "token":self.token,
                "type_obj":self.type_obj,
                "date_reg":self.date_reg,
                "status_reg":self.status_reg }

class Metrics (Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    access_date = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    access_page = Column(String(120), nullable=False)
    access_duration = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Metrics %r>' % self.id

    def to_json(self):
        return {"id":self.id,
                "access_date":self.access_date,
                "access_page":self.access_page,
                "access_duration":self.access_duration}
