from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    token = Column(String(80), nullable=False)
    profil_id = Column(Integer, ForeignKey('profil.id'), nullable=False, default=3)

    profil = relationship('Profil', back_populates='profils')

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
    id = Column(Integer, primary_key=True)
    description = Column(String(80), nullable=False)

    def __repr__(self):
        return '<Profil %r>' % self.description

    def to_json(self):
        return {"id":self.id,
                "description":self.description}

class Calcul(Base):
    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    result = Column(Integer)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    user = relationship('User', back_populates='users')

    def __repr__(self):
        return '<Calcul %r>' % self.name

    def to_json(self):
        return {"id":self.id,
                "description":self.body+" = "+ str(self.result),
                "date":self.date,
                "user_id":self.user_id}
