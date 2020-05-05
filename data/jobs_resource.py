from data.jobs import Jobs
from data.categories import Category
from data.users import User
from flask import jsonify
from data import db_session
from data.jobs_parser import parser
from flask_restful import reqparse, abort, Resource


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        return jsonify({'jobs': jobs.to_dict(only=('id',
                                                   'job',
                                                   'team_leader.name',
                                                   'team_leader.surname',
                                                   'work_size',
                                                   'collaborators',
                                                   'is_finished',
                                                   'categories_id'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id',
                  'job',
                  'team_leader.name',
                  'team_leader.surname',
                  'work_size',
                  'collaborators',
                  'is_finished',
                  'categories_id')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(args['id'])
        if job:
            abort(404, message=f"Id {args['id']} already exists")
        job = Jobs()
        job.job = args['job']
        job.id = args['id']
        job.team_leader_id = args['team_leader_id']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        job.team_leader = session.query(User).filter(User.id == args['team_leader_id']).first()
        job.categories_id = args['categories_id']
        session.add(job)
        session.commit()
        for i in args['categories_id'].split(', '):
            job.categories.append(session.query(Category).filter(Category.id == int(i)).first())
        session.commit()
        return jsonify({'success': 'OK'})