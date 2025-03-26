import flask
from flask import jsonify, make_response, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality',
                                    'address', 'email'))
                 for item in users]
        }
    )

@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}, 404))
    return jsonify(
        {
            'user':
                user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality',
                                    'address', 'email'))
        }
    )

@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in ['surname', 'name', 'age', 'position', 'speciality', 'address',
                                                 'email', 'hashed_password']):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    db_sess = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
    )
    user.set_password(request.json['hashed_password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})

@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}, 400))
    if not all([True if i in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email'] else False
                for i in request.json]):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}, 404))
    user.surname = request.json['surname'] if 'surname' in request.json.keys() else user.surname
    user.name = request.json['name'] if 'name' in request.json.keys() else user.name
    user.age = request.json['age'] if 'age' in request.json.keys() else user.age
    user.position = request.json['position'] if 'position' in request.json.keys() else user.position
    user.speciality = request.json['speciality'] if 'speciality' in request.json.keys() else user.speciality
    user.address = request.json['address'] if 'address' in request.json.keys() else user.address
    user.email = request.json['email'] if 'email' in request.json.keys() else user.email
    db_sess.commit()
    db_sess.close()


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}, 404))
    db_sess.delete(user)
    db_sess.commit()
    db_sess.close()