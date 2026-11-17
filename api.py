from main import app

from flask import request
from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse, inputs
from db import db, Blog

api = Api(app)

blog_args = reqparse.RequestParser()
blog_args.add_argument('title', type=str, required=True, help="Title cannot be blank")
blog_args.add_argument('subtitle', type=str, required=True, help="Subtitle cannot be blank")
blog_args.add_argument('author', type=str, required=True, help="author cannot be blank")
blog_args.add_argument('image_url', type=str, required=True, help="image url cannot be left blank")
blog_args.add_argument('body', type=str, required=True, help="Body cannot be blank")
blog_args.add_argument('date', type=str, required=True, help="publish date needs to be filled.")

blog_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'subtitle': fields.String,
    'author': fields.String,
    'image_url': fields.String,
    'body': fields.String,
    'date': fields.String,
}

class Blogs(Resource):
    @marshal_with(blog_fields)
    def get(self):
        all_blogs = Blog.query.all()
        return all_blogs

    @marshal_with(blog_fields)
    def post(self):
        args = blog_args.parse_args()
        new_blog = Blog(
            tile=args['title'],
            subtitle=args['subtitle'],
            author=args['author'],
            image_url=args['image_url'],
            body=args['body'],
            date=args['date'],
            )
        db.session.add(new_blog)
        db.session.commit()
        return new_blog, 201



class SingleBlog(Resource):
    @marshal_with(blog_fields)
    def get(self, blog_id):
        blog = db.get_or_404(Blogs,blog_id)
        return blog

    @marshal_with(blog_fields)
    def put(self, blog_id):
        args = blog_args.parse_args()
        blog = db.get_or_404(Blog, blog_id)

        blog.title = args['title']
        blog.subtitle = args['subtitle']
        blog.author = args['author']
        blog.image_url = args['image_url']
        blog.body = args['body']
        blog.date = args['date']
        
        db.session.commit()
        return blog, 200

    def delete(self, blog_id):
        blog = db.get_or_404(Blog, blog_id)

        db.session.delete(blog)
        db.session.commit()
        return {'return_value':"sucsessfully deleated"}, 204

api.add_resource(Blog, '/api/blog/')
api.add_resource(SingleBlog, '/api/blog/<int:blog_id>/')



