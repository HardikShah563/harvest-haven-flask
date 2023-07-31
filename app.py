from flask import Flask, url_for, request, redirect, flash, session
from flask.templating import render_template
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
# from database import *
import hashlib

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index(): 
    return render_template('home.html', session = session)

@app.route('/signin')
def signin(): 
    return render_template('signin.html')

@app.route('/signup')
def signup(): 
    return render_template('signup.html')

@app.route('/store')
def store(): 
    return render_template('store.html')

@app.route('/cart')
def store(): 
    return render_template('cart.html')

@app.route('/checkout')
def store(): 
    return render_template('checkout.html')

@app.route('/admin-dashboard')
def store(): 
    return render_template('adminDashboard.html')

@app.route('/admin-stats')
def store(): 
    return render_template('adminStats.html')

@app.route('/add-item')
def store(): 
    return render_template('addItem.html')

@app.route('/edit-item')
def store(): 
    return render_template('editItem.html')

@app.route('/delete-item')
def store(): 
    return render_template('deleteItem.html')

@app.route('/add-category')
def store(): 
    return render_template('addCategory.html')

@app.route('/edit-category')
def store(): 
    return render_template('editCategory.html')

@app.route('/delete-category')
def store(): 
    return render_template('deleteCategory.html')


if __name__ == '__main__': 
    app.run(debug = True)