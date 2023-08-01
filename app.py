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
    return render_template('signin.html', session = session)

@app.route('/signup')
def signup(): 
    return render_template('signup.html', session = session)

@app.route('/store')
def store(): 
    return render_template('store.html', session = session)

@app.route('/cart')
def cart(): 
    return render_template('cart.html', session = session)

@app.route('/checkout')
def checkout(): 
    return render_template('checkout.html', session = session)

@app.route('/admin-dashboard')
def adminDashboard(): 
    return render_template('adminDashboard.html', session = session)

@app.route('/admin-stats')
def adminStats(): 
    return render_template('adminStats.html', session = session)

@app.route('/add-item')
def addItem(): 
    return render_template('addItem.html', session = session)

@app.route('/edit-item')
def editItem(): 
    return render_template('editItem.html', session = session)

@app.route('/delete-item')
def deleteItem(): 
    return render_template('deleteItem.html', session = session)

@app.route('/add-category')
def addCategory(): 
    return render_template('addCategory.html', session = session)

@app.route('/edit-category')
def editCategory(): 
    return render_template('editCategory.html', session = session)

@app.route('/delete-category')
def deleteCategory(): 
    return render_template('deleteCategory.html', session = session)


if __name__ == '__main__': 
    app.run(debug = True)