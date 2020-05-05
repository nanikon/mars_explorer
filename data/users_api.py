import flask

from flask import jsonify, request
from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/user')
def get_jobs():
    session = db_session.create_session()
    user = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id',
                                    'surname',
                                    'name',
                                    'age',
                                    'position',
                                    'speciality',
                                    'address',
                                    'city_from',
                                    'email',
                                    'modified_date'))
                 for item in user]
        }
    )


@blueprint.route('/api/user/<int:user_id>',  methods=['GET'])
def get_one_job(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id',
                                       'surname',
                                       'name',
                                       'age',
                                       'position',
                                       'speciality',
                                       'address',
                                       'city_from',
                                       'email',
                                       'modified_date'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id',
                  'surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'password',
                  'email',
                  'city_from']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    user = User()
    user.id = request.json['id']
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.city_from = request.json['city_from']
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>',  methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.surname = request.json.get('surname', user.surname)
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.position = request.json.get('position', user.position)
    user.speciality = request.json.get('speciality', user.speciality)
    user.address = request.json.get('address', user.address)
    user.city_from = request.json.get('city_from', user.city_from)
    user.email = request.json.get('email', user.email)
    if 'password' in request.json:
        user.set_password(request.json['password'])
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_job(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})
