from flask import Flask, request, render_template, url_for

app = Flask(__name__)


@app.route('/index/<title>', methods=['GET'])
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>', methods=['GET'])
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<param>', methods=['GET'])
def prof_list(param):
    query = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
             'инженер по терраформированию', 'климатолог', 'специалист по радиационной защите',
             'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
             'киберинженер', 'штурман', 'пилот дронов']
    return render_template('profession_list.html', param=param, query=query)


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



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
