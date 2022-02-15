from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String(150))
    name_last = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    wins = db.Column(db.Integer,default=0)
    losses = db.Column(db.Integer,default=0)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    pokemen = db.relationship('Pokemon', secondary='user_join_pokemon', backref='users',lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.name_first = data['name_first']
        self.name_last = data['name_last']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # saves user to database
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def poke_count(self):
        if len(list(self.poke_dictionary)) <= 5:
            pass
        
    def exists(self,name):
        if Pokemon.query.filter_by(name=name).first() in self.pokemen:
            return True 
        return False
    
    # def exists2(name):
    #     if User.pokemen.query.filter_by(name=name).first():
    #         pass
    
    def get_id(self):
        return self.user_id
        
class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    order = db.Column(db.Integer)
    ability = db.Column(db.String(50))
    base_experience = db.Column(db.Integer)
    front_shiny = db.Column(db.String)
    stat_name1 = db.Column(db.String(50))
    stat_rating1 = db.Column(db.Integer)
    stat_name2 = db.Column(db.String(50))
    stat_rating2 = db.Column(db.Integer)
    stat_name3 = db.Column(db.String(50))
    stat_rating3 = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
        
    def poke_dictionary(self, data):
        self.name = data['name']
        self.order = data['order']
        self.ability = data['ability']
        self.base_experience = data['base_experience']
        self.front_shiny = data['front_shiny']
        self.stat_name1 = data['stat_name1']
        self.stat_rating1 = data['stat_rating1']
        self.stat_name2 = data['stat_name2']
        self.stat_rating2 = data['stat_rating2']
        self.stat_name3 = data['stat_name3']
        self.stat_rating3 = data['stat_rating3']

    def __repr__(self):
        return f'<Post: {self.id} | {self.name}>'
    
    def save(self):
        db.session.add(self) # add the pokemon to the db session
        db.session.commit() #save everything in the session to the database
        
    def exists(name):
        return Pokemon.query.filter_by(name=name).first()
            
    def delete(poke_id):
        db.session.remove(poke_id) # remove the pokemon from the db session add the pokemon to the db session
        db.session.commit() #save everything in the session to the database
    
    def get_poke_id(self):
        return self.poke_id
        
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserJoinPokemon(db.Model):
    poke_id = db.Column(db.Integer, db.ForeignKey(Pokemon.poke_id, ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
        
    def save(self):
        db.session.add(self) # add the pokemon to the db session
        db.session.commit() #save everything in the session to the database
    