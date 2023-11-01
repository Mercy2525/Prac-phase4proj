from flask import Flask
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Blog, Comment, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True
migrate = Migrate(app,db,render_as_batch=True)


db.init_app(app)
api = Api(app)


class Blogres(Resource):
    def get(self):
        blog_dict=[n.to_dict() for n in Blog.query.all()]
        response = make_response(
            jsonify(blog_dict),200
        )
        return response
 

    def post(self):
        data = request.get_json()        
        newrec= Blog(
            author=data.get('author'),
            blog_title=data.get('blog_title'),
            blog_body=data.get('blog_body'),
        )

        db.session.add(newrec)
        db.session.commit() 

        newrec_dict=newrec.to_dict()

        return make_response(
            jsonify({"message": newrec_dict,"message": "Blog has been created successfully" }),200)

api.add_resource(Blogres, '/blog', endpoint='blog')


class BlogById(Resource):
    def get(self,id):
        blog= Blog.query.filter_by(id=id).first()

        if not blog:
            return {"error": "Blog not found"}, 404

        
        blog_dict=blog.to_dict()

        response=make_response(jsonify(blog_dict),200)
        return response
    
    def patch(self,id):
        blog= Blog.query.filter_by(id=id).first()

        if not blog:
            return {"error": "Blog not found"}, 404


        for attr in request.get_json():
            setattr(blog,attr,request.get_json()[attr])

            db.session.add(blog)
            db.session.commit()

            user_dict=blog.to_dict()

            response = make_response(jsonify(user_dict),200)
            return response


    def delete(self,id):
        blog= Blog.query.filter_by(id=id).first() 

        if not blog:
            return {"error": "Blog not found"}, 404

        db.session.delete(blog)
        db.session.commit()

        response_body={"message": "Blog deleted successfully"},200
        return response_body
    
api.add_resource(BlogById,'/blog/<int:id>', endpoint='blogid')

class Users(Resource):
    def get(self):
        users=[user.to_dict() for user in User.query.all()]


        response=make_response(jsonify(users), 200)
        return response
    
api.add_resource(Users,'/users', endpoint='users')

class Comments(Resource):
    def get(self):
        comments=[comment.to_dict() for comment in Comment.query.all()]

        response=make_response(jsonify(comments),200)

        return response
    
    def post(self):
        new_comment=Comment(
            comment_body=request.get_json()['comment_body'],
            user_id= request.get_json()['user_id'],
            blog_id= request.get_json()['blog_id']
        )

        db.session.add(new_comment)
        db.session.commit()

        new_comment_dict=new_comment.to_dict()

        response=make_response(jsonify(new_comment_dict),201)
        return response
             
    
api.add_resource(Comments, '/comments', endpoint='comments')

class CommentById(Resource):
    def get(self,id):
        comment = Comment.query.filter_by(id=id).first()
        if not comment:
           return("comment not found"),404
        comment_to_dict= comment.to_dict()
        response = make_response(jsonify(comment_to_dict),201)
        return response 
    

    def patch(self,id):
        comment = Comment.query.filter_by(id=id).first()
        if not comment:
            return ('comment not found'), 404
        
        for attr in request.get_json():
            setattr(comment,attr,request.get_json()[attr])

            db.session.add(comment)
            db.session.commit()

            comment_dict=comment.to_dict()

            response=make_response(jsonify(comment_dict),201)

            return response


    def delete(self,id):
        comment = Comment.query.filter_by(id=id).first()
        if not comment:
            return("comment not found"),404
        db.session.delete(comment)
        db.session.commit()
        response = make_response({"message": "comment deleted successfully"},200)
        return response

        
api.add_resource(CommentById,'/comment/<int:id>', endpoint='comment')
 


if __name__=='__main__':
    app.run(debug=True, port=5000)
