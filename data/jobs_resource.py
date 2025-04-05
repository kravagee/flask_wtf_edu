from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.jobs import Jobs


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    news = session.query(Jobs).get(job_id)
    if not news:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.close()
        return jsonify({'job': job.to_dict(
            only=('teamleader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')
        )})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        session.close()


parser = reqparse.RequestParser()
parser.add_argument('teamleader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True)
parser.add_argument('end_date', required=True)
parser.add_argument('is_finished', required=True, type=int)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        session.close()
        return jsonify({'jobs': [item.to_dict(
            only=('teamleader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
            for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            teamleader=args['teamleader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})