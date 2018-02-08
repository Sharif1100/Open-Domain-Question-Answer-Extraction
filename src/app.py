from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

import re
import gevent.monkey
from gevent.pywsgi import WSGIServer

from find_answer import answer_question


class QuestionForm(Form):
    question = StringField('', validators=[InputRequired()])
    submit_button = SubmitField('Ask Me')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    Bootstrap(app)

    app.config['SECRET_KEY'] = "b'\xa4\xe3]\x7f)\xc5\xfbQ\x9f\x1d{\xfc\xa8\x81J\n"

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/ask_me', methods=('GET', 'POST'))
    def ask_me():
        if request.method == 'POST':
            try:
                question = request.form['question']
            except KeyError as e:
                print('key error')
                print('I got a KeyError - reason "%s"' % str(e))
            except:
                print('I got another exception, but I should re-raise')
                raise

            print(question)
            answer = answer_question(question)

            print('answer: ', answer)
            answer = re.sub('([(].*?[)])', "", answer)

            return render_template('answer.html', answer=answer, question=question)

        form = QuestionForm()
        return render_template('ask_me.html', form=form)

    return app


app = create_app()

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 9191), app)
    print("starting server on port 9191")
    http_server.serve_forever()
    # app.run(debug=True)
