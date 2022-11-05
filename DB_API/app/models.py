from database_init import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date
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