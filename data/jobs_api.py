import flask

from flask import jsonify, request
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.categories import Category

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id',
                                    'job',
                                    'team_leader.name',
                                    'team_leader.surname',
                                    'work_size',
                                    'collaborators',
                                    'is_finished',
                                    'categories_id'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>',  methods=['GET'])
def get_one_job(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id',
                                       'job',
                                       'team_leader.name',
                                       'team_leader.surname',
                                       'work_size',
                                       'collaborators',
                                       'is_finished',
                                       'categories_id'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader_id', 'work_size', 'collaborators', 'categories_id', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    job = Jobs()
    job.job = request.json['job']
    job.id = request.json['id']
    job.team_leader_id = request.json['team_leader_id']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    job.team_leader = session.query(User).filter(User.id == request.json['team_leader_id']).first()
    job.categories_id = request.json['categories_id']
    session.add(job)
    session.commit()
    for i in request.json['categories_id'].split(', '):
        job.categories.append(session.query(Category).filter(Category.id == int(i)).first())
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>',  methods=['PUT'])
def edit_job(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    job.job = request.json.get('job', job.job)
    job.team_leader_id = request.json.get('team_leader_id', job.team_leader_id)
    job.team_leader = session.query(User).filter(User.id == job.team_leader_id).first()
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.is_finished = request.json.get('is_finished', job.is_finished)
    if 'categories_id' in request.json:
        for i in job.categories_id.split(', '):
            job.categories.remove(session.query(Category).filter(Category.id == int(i)).first())
        session.commit()
        job.categories_id = request.json['categories_id']
        for i in request.json['categories_id'].split(', '):
            job.categories.append(session.query(Category).filter(Category.id == int(i)).first())
    session.commit()
    return jsonify({'success': 'OK'})