from data.users import User
from flask import jsonify
from data import db_session
from data.users_parser import parser
from flask_restful import reqparse, abort, Resource


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=('id',
                                                   'surname',
                                                   'name',
                                                   'age',
                                                   'position',
                                                   'speciality',
                                                   'address',
                                                   'city_from',
                                                   'email',
                                                   'modified_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id',
                  'surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'city_from',
                  'email',
                  'modified_date')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(args['id'])
        if user:
            abort(404, message=f"Id {args['id']} already exists")
        user = User()
        user.id = args['id']
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.city_from = args['city_from']
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})