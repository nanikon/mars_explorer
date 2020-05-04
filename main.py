from flask import Flask, render_template

from data import db_session
from data.users import User
from data.jobs import Jobs

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
    submit = SubmitField('Submit')


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template('works.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
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
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        message = 'Колонист ' + form.surname.data + ' ' + form.name.data + ' успешно занесен в нашу БД. Не желаете зарегистрировать ещё одного, пока мы готовим форму для авторизации?'
    return render_template('register.html', form=form, message=message)


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.sqlite")
    app.run(port=8080, host='127.0.0.1')