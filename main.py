from flask import Flask, render_template

from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template('works.html', jobs=jobs)


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.sqlite")
    app.run(port=8080, host='127.0.0.1')