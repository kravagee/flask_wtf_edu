import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('teamleader', 'job',
                                    'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                 for item in jobs]
        }
    )

@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}, 404))
    return jsonify(
        {
            'job': job.to_dict(only=('teamleader', 'job',
                                    'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
        }
    )

@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}, 400))
    elif not all(key in request.json for key in ['teamleader', 'job',
                                    'work_size', 'collaborators', 'start_date', 'end_date']):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    db_sess = db_session.create_session()
    job = Jobs(
        teamleader=request.json['teamleader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}, 400))
    if not all([True if i in ['job', 'teamleader', 'work_size', 'collaborators', 'start_date',
                              'end_date', 'is_finished'] else False
                for i in request.json]):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Job not found'}, 404))
    job.job = request.json['job'] if 'job' in request.json.keys() else job.job
    job.teamleader = request.json['teamleader'] if 'teamleader' in request.json.keys() else job.teamleader
    job.work_size = request.json['work_size'] if 'work_size' in request.json.keys() else job.work_size
    job.collaborators = request.json['collaborators'] if 'collaborators' in request.json.keys() else job.collaborators
    job.start_date = request.json['start_date'] if 'start_date' in request.json.keys() else job.start_date
    job.end_date = request.json['end_date'] if 'end_date' in request.json.keys() else job.end_date
    job.is_finished = request.json['is_finished'] if 'is_finished' in request.json.keys() else job.is_finished
    db_sess.commit()
    db_sess.close()