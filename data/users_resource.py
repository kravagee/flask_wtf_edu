from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.close()
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email')
        )})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({'succes': 'ok'})


parser = reqparse.RequestParser()
parser.add_argument('surname', requried=True)
parser.add_argument('name', required=True)
parser.add_argument('age', requried=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', requried=True)
parser.add_argument('address', required=True)
parser.add_argument('email', requried=True)
parser.add_argument('password', required=True)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        session.close()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
            for item in users
        ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        session.close()
        return jsonify({'id': user.id})