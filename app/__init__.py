import os
from flask import Flask, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from app.controllers import users
from app.controllers import expenses

@app.route('/')
def index():
    return redirect('/login_register')
