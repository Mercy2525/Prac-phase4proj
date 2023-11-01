from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask import Flask  
from models import User, Blog, Comment, db
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)

with app.app_context():
    user1 = User(name='User1', username='user1')
    user2 = User(name='User2', username='user2')
    blog1 = Blog(blog_title='Blog Title 1', blog_body='This is the first blog.', author='Author 1')
    blog2 = Blog(blog_title='Blog Title 2', blog_body='Another interesting blog post.', author='Author 1')
    blog3 = Blog(blog_title='Blog Title 3', blog_body='A blog post by user2.', author='Author 2')

    comment1 = Comment(comment_body='Great blog post!', user=user1, blog=blog1)
    comment2 = Comment(comment_body='I enjoyed reading this.', user=user2, blog=blog1)
    comment3 = Comment(comment_body='Nice post!', user=user1, blog=blog2)
    comment4 = Comment(comment_body='Interesting thoughts.', user=user2, blog=blog3)

    print("Database initialization in progress...")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(blog1)
    db.session.add(blog2)
    db.session.add(blog3)
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.add(comment3)
    db.session.add(comment4)

    db.session.commit()

    print("Database initialization completed.")
