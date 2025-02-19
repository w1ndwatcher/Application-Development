from flask_restful import Resource, Api, reqparse, fields, marshal_with
from .models import db, Section
from .instances import cache
from flask_security import auth_required, roles_required, current_user
from flask import request

api = Api(prefix='/api')

# section
section_parser = reqparse.RequestParser()
section_parser.add_argument('section_name', type=str, help='Name of the Section should be a string.', required=True)
section_parser.add_argument('section_icon', type=str, help='Description of the Section should be a string.')
section_parser.add_argument('description', type=str, help='Description of the Section should be a string.')

section_fields = {
    'id': fields.Integer,
    'section_name': fields.String,
    'section_icon': fields.String,
    'description': fields.String,
    'created_by': fields.String,
    'date_created': fields.DateTime,
    'updated_by': fields.String,
    'updated_date': fields.DateTime
}

class BookSection(Resource):
    @auth_required('token')
    @marshal_with(section_fields)
    @cache.cached(timeout=30)
    def get(self):
        all_sections = Section.query.all()
        print(all_sections)
        return all_sections, 200
    
    @auth_required('token')
    @roles_required('librarian')
    def post(self):
        user = current_user
        args = section_parser.parse_args() 
        args['created_by'] = user.username
        newsection = Section(**args)
        db.session.add(newsection)
        db.session.commit()
        cache.clear()
        return {'message': 'Section created successfully.'}, 200
    
    @auth_required('token')
    @roles_required('librarian')
    def put(self):
        secid = request.args.get('secid')
        user = current_user
        section = Section.query.get(secid)
        print(secid)
        print(section)
        if not section:
            return {"message": "Section not found!"}, 400
        args = section_parser.parse_args()
        print(args)
        section.section_name = args['section_name']
        section.section_icon = args['section_icon']
        section.description = args['description']
        section.updated_by = user.username
        db.session.commit()
        cache.clear()
        newsection = {
            'id': section.id,
            'section_name': section.section_name,
            'section_icon': section.section_icon,
            'description': section.description
        }
        print(newsection)
        return newsection, 200
    
    @auth_required('token')
    @roles_required('librarian')
    def delete(self):
        secid = request.args.get('secid')
        user = current_user
        section = Section.query.get(secid)
        if not section:
            return {"message": "Section not found!"}, 400
        db.session.delete(section)
        db.session.commit()
        cache.clear()
        return {'message': 'Section deleted.'}, 200
            
api.add_resource(BookSection, '/manage_section')