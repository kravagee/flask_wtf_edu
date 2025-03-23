from flask import Flask, request, render_template, url_for, make_response, jsonify, redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from data import jobs_api, db_session, users_api
from data.jobs import Jobs
from data.users import User
from forms.job import AddJobForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


@app.route('/list_prof/<param>', methods=['GET'])
@login_required
def prof_list(param):
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs).all()
    return render_template('profession_list.html', param=param, query=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User()
        new_user.surname = request.form['surname']
        new_user.name = request.form['name']
        new_user.age = request.form['age']
        new_user.position = request.form['position']
        new_user.speciality = request.form['speciality']
        new_user.address = request.form['address']
        new_user.email = request.form['email']
        new_user.hashed_password = request.form['hashed_password']
        db_sess = db_session.create_session()
        db_sess.add(new_user)
        db_sess.commit()
        db_sess.close()
        login_user(new_user)
        return redirect(url_for('prof_list', param='ul'))

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        surname = request.form['surname']
        db_sess = db_session.create_session()
        data = db_sess.query(User).filter(User.name == name, User.surname == surname,
                                          User.email == email).first()
        if not data:
            return make_response(jsonify({'error': 'User not found'}, 404))
        if data.check_password(password):
            login_user(data)
            return redirect(url_for('prof_list', param='ul'))
        return make_response(jsonify({'error': 'Wrong password'}, 200))
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['POST', 'GET'])
@login_required
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        new_job = Jobs()
        new_job.teamleader = request.form['teamleader']
        new_job.job = request.form['job']
        new_job.work_size = request.form['work_size']
        new_job.collaborators = request.form['collaborators']
        new_job.start_date = request.form['start_date']
        new_job.end_date = request.form['end_date']
        db_sess = db_session.create_session()
        db_sess.add(new_job)
        db_sess.commit()
        db_sess.close()
        return redirect(url_for('prof_list', param='ul'))


if __name__ == '__main__':
    db_session.global_init('db/mars_explorer.db')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
