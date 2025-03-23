from flask import Flask, request, render_template, url_for, make_response, jsonify, redirect

from data import jobs_api, db_session
from data.jobs import Jobs
from data.users import User
from forms.job import AddJobForm
from forms.user import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/index/<title>', methods=['GET'])
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>', methods=['GET'])
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<param>', methods=['GET'])
def prof_list(param):
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs).all()
    return render_template('profession_list.html', param=param, query=data)


@app.route('/anwser', methods=['GET'])
def anwser():
    params = {'title': 'Анкета',
              'surname': 'Васильев',
              'name': 'Василий',
              'education': 'средний',
              'profession': 'сборщик мусора',
              'sex': 'male',
              'motivation': ' фзывтипсомиикцнге',
              'ready': True}
    return render_template('auto_anwser.html', **params)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        surname = request.form['surname']
        if password and name and email and surname:
            db_sess = db_session.create_session()
            data = db_sess.query(User).filter(User.name == name, User.surname == surname,
                                              User.email == email).first()
            if not data:
                return make_response(jsonify({'error': 'User not found'}, 404))
            if data.hashed_password == password:
                return redirect(url_for('prof_list', param='ul'))
        return make_response(jsonify({'error': 'Not found'}, 404))
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/addjob', methods=['POST', 'GET'])
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        new_job = Jobs()
        if request.form['teamleader'] and request.form['job'] and request.form['work_size'] \
            and request.form['collaborators'] and request.form['start_date'] and request.form['end_date']:

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
    app.run(port=8080, host='127.0.0.1')
