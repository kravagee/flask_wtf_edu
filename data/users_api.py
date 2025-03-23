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
        hashed_password=request.json['hashed_password']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})

@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}, 400))
    print(request.json)
    db_session.create_session()