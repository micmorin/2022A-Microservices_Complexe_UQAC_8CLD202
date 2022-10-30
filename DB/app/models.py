from database_init import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(80), nullable=False)
    profil_id = db.Column(db.Integer, db.ForeignKey('profil.id'), nullable=False, default=3)

    profil = db.relationship('Profil', backref='profils')

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

class Profil (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Profil %r>' % self.description

    def to_json(self):
        return {"id":self.id,
                "description":self.description}

class Calcul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    result = db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<Calcul %r>' % self.name

    def to_json(self):
        return {"id":self.id,
                "description":self.body+" = "+ str(self.result),
                "date":self.date,
                "user_id":self.user_id}