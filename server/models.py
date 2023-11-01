from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt=Bcrypt()
 


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-comments.user',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    comments = db.relationship('Comment', backref='user')
    _password_hash = db.Column(db.String)
   

     
    @hybrid_property
    def password_hash(self):
        # return self._password_hash
        raise AttributeError('should not view password_hash')
    
    @password_hash.setter
    def password_hash(self, password):       
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
        

class Blog(db.Model, SerializerMixin):
    __tablename__ = 'blogs'
    serialize_rules = ('-comments.blog',)

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String)
    blog_body = db.Column(db.String)
    author = db.Column(db.String)
    comments = db.relationship('Comment', backref='blog')

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'
    serialize_rules = ('-user.comments', '-blog.comments',)

    id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
