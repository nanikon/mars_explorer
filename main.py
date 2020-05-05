from flask import Flask, render_template, redirect, request, abort, make_response, jsonify

from data import db_session, jobs_api, users_api, users_resource, jobs_resource
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.categories import Category

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user
from flask_login import login_required, logout_user, current_user

from requests import get

from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('PasswordField', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    specially = StringField('Specially', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city_from = StringField('City_from', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class JobForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    team_leader_id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborator = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    categories_id = StringField('Categories id', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


class DepartmentForm(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    chief_id = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Department email', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template('index.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.specially.data
        user.address = form.address.data
        user.email = form.email.data
        user.city_from = form.city_from.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.team_leader_id = form.team_leader_id.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborator.data
        job.is_finished = form.is_finished.data
        job.team_leader = session.query(User).filter(User.id == form.team_leader_id.data).first()
        job.categories_id = form.categories_id.data
        session.add(job)
        session.commit()
        for i in form.categories_id.data.split(', '):
            job.categories.append(session.query(Category).filter(Category.id == int(i)).first())
        session.commit()
        return redirect('/')
    return render_template('adding_job.html', title="Adding a Job", form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.team_leader == current_user) | (current_user.id == 1))).first()
        if job:
            form.team_leader_id.data = job.team_leader_id
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborator.data = job.collaborators
            form.is_finished.data = job.is_finished
            form.categories_id.data = job.categories_id
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.team_leader == current_user) | (current_user.id == 1))).first()
        if job:
            job.team_leader_id = form.team_leader_id.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborator.data
            job.is_finished = form.is_finished.data
            job.team_leader = session.query(User).filter(User.id == form.team_leader_id.data).first()
            for i in job.categories_id.split(', '):
                job.categories.remove(session.query(Category).filter(Category.id == int(i)).first())
            session.commit()
            job.categories_id = form.categories_id.data
            for i in form.categories_id.data.split(', '):
                job.categories.append(session.query(Category).filter(Category.id == int(i)).first())
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('adding_job.html', title='Editing a Job', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id,
                                     ((Jobs.team_leader == current_user) | (current_user.id == 1))).first()
    if job:
        for i in job.categories_id.split(', '):
            job.categories.remove(session.query(Category).filter(Category.id == int(i)).first())
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    session = db_session.create_session()
    dep = session.query(Department)
    return render_template('departments_list.html', departments=dep, title='List of Departments')


@app.route('/department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief_id = form.chief_id.data
        dep.chief = session.query(User).filter(User.id == form.chief_id.data).first()
        dep.members = form.members.data
        dep.email = form.email.data
        session.add(dep)
        session.commit()
        return redirect('/departments')
    return render_template('departments.html', form=form, title="Add a Department")


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepartmentForm()
    if request.method == 'GET':
        session = db_session.create_session()
        dep = session.query(Department).filter(Department.id == id,
                                               ((Department.chief == current_user) | (current_user.id == 1))).first()
        if dep:
            form.title.data = dep.title
            form.chief_id.data = dep.chief_id
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = session.query(Department).filter(Department.id == id,
                                               ((Department.chief == current_user) | (current_user.id == 1))).first()
        if dep:
            dep.title = form.title.data
            dep.chief_id = form.chief_id.data
            dep.chief = session.query(User).filter(User.id == form.chief_id.data).first()
            dep.members = form.members.data
            dep.email = form.email.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('departments.html', form=form, title='Editing a Department')


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    session = db_session.create_session()
    dep = session.query(Department).filter(Department.id == id,
                                           ((Department.chief == current_user) | (current_user.id == 1))).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/users_show/<int:user_id>')
def nostalgy(user_id):
    user = get('http://127.0.0.1:8080/api/user/' + str(user_id)).json()['user']
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-" + \
                       "98533de7710b&geocode=" + user['city_from'] + "&format=json"
    response = get(geocoder_request)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = ','.join(i for i in toponym["Point"]["pos"].split())
    image_link = "https://static-maps.yandex.ru/1.x/?ll=" + toponym_coodrinates + "&spn=0.1,0.1&l=sat"
    return render_template('nostalgia.html', title='Hometown', user=user, image_link=image_link)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    app.run(port=8080, host='127.0.0.1')