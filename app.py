from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/index/<title>', methods=['GET'])
def index(title):
    return render_template('base.html', title=title)

@app.route('/training/<prof>', methods=['GET'])
def training(prof):
    return render_template('training.html', prof=prof)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
