from flask import Flask, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

from app.controllers import users
from app.controllers import expenses

@app.route('/')
def index():
    return redirect('/login_register')
