#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


# @app.route('/')
# def home():
#     return ''
class Home(Resource):
    def get(self):
        response_dict = {
            'message': 'bro, this shit is working so well.'
        }
        return make_response(response_dict, 200)


api.add_resource(Home, '/')


class Scientists(Resource):
    def get(self):
        response_dict_list = [s.to_dict() for s in Scientist.query.all()]
        return make_response(response_dict_list, 200)

    def post(self):
        request_object = request.get_json()
        try:
            new_scientist = Scientist(
                name=request_object['name'],
                field_of_study=request_object['field_of_study']
            )
            db.session.add(new_scientist)
            db.session.commit()
        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_scientist.to_dict(), 201)


api.add_resource(Scientists, '/scientists')


class ScientistsById(Resource):
    def get(self, id):
        response_obj = Scientist.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                "error": "Scientist not found"
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(rules=('mission_field',)), 200)

    def patch(self, id):
        response_obj = Scientist.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                "error": "Scientist not found"
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])
                    db.session.add(response_obj)
                    db.session.commit()
            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)

    def delete(self, id):
        response_obj = Scientist.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                "error": "Scientist not found"
            }
            return make_response(response_dict, 404)
        else:
            db.session.delete(response_obj)
            db.session.commit()
            response_dict = {'message': 'deleted fo sho!'}
            return response_dict, 200


api.add_resource(ScientistsById, '/scientists/<int:id>')


class Planets(Resource):
    def get(self):
        response_dict_list = [p.to_dict() for p in Planet.query.all()]
        return make_response(response_dict_list, 200)


api.add_resource(Planets, '/planets')


class Missions(Resource):
    def get(self):
        response_dict_list = [m.to_dict() for m in Mission.query.all()]
        return make_response(response_dict_list, 200)

    def post(self):
        request_object = request.get_json()
        try:
            new_mission = Mission(
                name=request_object['name'],
                scientist_id=request_object['scientist_id'],
                planet_id=request_object['planet_id']
            )
            db.session.add(new_mission)
            db.session.commit()
        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_mission.to_dict(rules=('planet_field', 'scientist_field')), 201)


api.add_resource(Missions, '/missions')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
