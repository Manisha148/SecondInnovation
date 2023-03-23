from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import openai
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
app.config["Debug"] = True

# openai.api_key_path='apikey'
openai.api_key = os.environ.get('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError('API_KEY environment variable is not set')

class MyFlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route('/')(self.index)
        self.route('/output', methods=['GET'])(self.output)
        self.register_error_handler(404, self.page_not_found)

    def index(self):
        return render_template('index.html')
    
    def users():
    users = User.query.all()
    return jsonify([{'name': u.name, 'email': u.email} for u in users])
    

    def page_not_found(self, e):
        return render_template('404.html'), 404

    def output(self):
        userInput = request.args.get('user-input')
        prompt = f"Generate a program to {userInput}."
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        program = response.choices[0].text.strip()
        return render_template('output.html', program=program)

if __name__ == '__main__':
    app = MyFlaskApp(__name__)
    app.run(host='0.0.0.0', port='8888', debug=True)
