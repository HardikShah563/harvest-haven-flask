from flask import Flask, url_for, request, redirect, flash, session
from flask.templating import render_template
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from database import *
import hashlib

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home(): 
    return render_template('home.html', session = session)

@app.route('/signin', methods=["POST", "GET"])
def signin():
    msgColor = ""
    msgText = ""
    if request.method == 'POST': 
        email = request.form['email']
        # passcode = hash(request.form['passcode'])
        passcode = hashlib.sha256(request.form['passcode'].encode('utf-8')).hexdigest()
        msg = loginAccount(email, passcode)
        if(msg): 
            msgColor = "green"
            msgText = "Login Successful!" 
            setSession(getUID(email), getName(email), email, adminCheck(email))
        else: 
            msgColor = "red"
            msgText = "Couldn't log you in, try again!"
    if session['u_id']: 
        return redirect("/")
    
    return render_template('signin.html', msgColor = msgColor,  msg = msgText, session = session)

# -------------------------------------------------------

@app.route('/signup', methods=["POST", "GET"])
def signup(): 
    msg = False
    msgColor = ""
    msgText = ""
    if request.method == 'POST': 
        name = request.form['name']
        email = request.form['email']
        if request.form['gender'] == "Male": 
            gender = True
        else: 
            gender = False
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        msg = registerAccount(name, gender, email, password)
        print(msg)
        if(msg == None): 
            msgColor = "green"
            msgText = "New Account Registered!"

        else: 
            msgColor = "red"
            msgText = "Email Already exists! Log in if you have an account!"

        setSession(getUID(email), name, email, adminCheck(email))
    
    # if the user has already logged in, he/she cannot visit the login/registeration page
    if session['u_id']: 
        return redirect("/")
    
    return render_template('signup.html', msgColor = msgColor, msg = msgText, session = session)

# -------------------------------------------------------

@app.route('/store')
def store(): 
    categories = getCategories()
    categoryIDs = getCategoryID()
    allItems = getAllItemsFromDB()
    
    return render_template('store.html', categories = categories, categoryIDs = categoryIDs, allItems = allItems, session = session)

# -------------------------------------------------------

@app.route('/cart')
def cart(): 
    return render_template('cart.html', session = session)

# -------------------------------------------------------

@app.route('/checkout')
def checkout(): 
    return render_template('checkout.html', session = session)

# -------------------------------------------------------

@app.route('/admin-dashboard')
def adminDashboard(): 
    categories = getCategories()
    categoryIDs = getCategoryID()
    allItems = getAllItemsFromDB()
    return render_template('adminDashboard.html', categories = categories, categoryIDs = categoryIDs, allItems = allItems, session = session)

# -------------------------------------------------------

@app.route('/admin-stats')
def adminStats(): 
    return render_template('adminStats.html', session = session)

# -------------------------------------------------------

@app.route('/add-item', methods=["GET", "POST"])
def addItem(): 
    msgColor = ""
    msgText = ""
    categories = getCategories()
    categoryIDs = getCategoryID()

    if request.method == 'POST': 
        pName = request.form['p_name']
        pQty = request.form['p_qty']
        pPrice = request.form['p_price']
        pStockQty = request.form['p_stock_qty']
        pImg = request.files['p_img'].read()
        cID = request.form['c_id']

        msg = putItems(pName, pQty, pPrice, pStockQty, pImg, cID)
        print(msg)
        if(msg == None): 
            msgColor = "green"
            msgText = "New Item Created!"

        else: 
            msgColor = "red"
            msgText = "Failed to create item, try again!"
    
    return render_template('addItem.html', msgColor = msgColor, msg = msgText, categories = categories, categoryIDs = categoryIDs, session = session)

# -------------------------------------------------------

@app.route('/edit-item')
def editItem(): 
    msgColor = ""
    msgText = ""
    msg = ""

    if(msg == None): 
        msgColor = "green"
        msgText = "Success!"

    else: 
        msgColor = "red"
        msgText = "Reject!"
    return render_template('editItem.html', msgColor = msgColor, msg = msgText, session = session)

# -------------------------------------------------------

@app.route('/delete-item', methods=["GET", "POST"])
def deleteItem(): 
    msgColor = ""
    msgText = ""
    msg = ""
    allItems = getAllItemNamesAndIDs()
    if request.method == "POST": 
        p_id = request.form["p_id"]
        msg = deleteProduct(p_id)
        print(msg)
        if(msg == None): 
            msgColor = "green"
            msgText = "Product successfully deleted!"

        else: 
            msgColor = "red"
            msgText = "Failed to delete the product!"
    return render_template('deleteItem.html', msgColor = msgColor, msg = msgText, allItems = allItems, session = session)

# -------------------------------------------------------

@app.route('/add-category', methods=["GET", "POST"])
def addCategory(): 
    msgColor = ""
    msgText = ""
    msg = ""

    if(msg == None): 
        msgColor = "green"
        msgText = "Success!"

    else: 
        msgColor = "red"
        msgText = "Reject!"
    return render_template('addCategory.html', msgColor = msgColor, msg = msgText, session = session)

# -------------------------------------------------------

@app.route('/edit-category', methods=["GET", "POST"])
def editCategory(): 
    msgColor = ""
    msgText = ""
    msg = ""
    categories = getCategories()
    categoryIDs = getCategoryID()

    if request.method == "POST": 
        oldID = request.form["old_name"]
        newName = request.form["new_name"]
        msg = editCategoryName(oldID, newName)
        if(msg == None): 
            msgColor = "green"
            msgText = "Category Name changed successfully!"

        else: 
            msgColor = "red"
            msgText = "Couldn't change Category Name!"
    return render_template('editCategory.html', msgColor = msgColor, msg = msgText, categories = categories, categoryIDs = categoryIDs, session = session)

# -------------------------------------------------------

@app.route('/delete-category', methods=["GET", "POST"])
def deleteCategory(): 
    msgColor = ""
    msgText = ""
    msg = ""
    categories = getCategories()
    categoryIDs = getCategoryID()

    if request.method == "POST": 
        c_id = request.form["c_id"]
        msg = deleteCategoryCompletely(c_id)
        if(msg == None): 
            msgColor = "green"
            msgText = "Category deleted successfully!"

        else: 
            msgColor = "red"
            msgText = "Couldn't delete Category!"
    return render_template('deleteCategory.html', msgColor = msgColor, msg = msgText, categories = categories, categoryIDs = categoryIDs, session = session)

# -------------------------------------------------------

@app.route('/signout')
def signout(): 
    destroySession()
    return redirect("/")

# -------------------------------------------------------

def updateCart(p_id, action): 
    flag = True
    for key in session['cart'].keys(): 
        if key == p_id: 
            if action == 'plsu':
                key[p_id] += 1
            if action == 'minus': 
                key[p_id] -= 1
            flag = False
    if flag: 
        session['cart'][p_id] = 1

# -------------------------------------------------------

# function for setting the session variables
def setSession(u_id, name, email, isAdmin): 
    session['u_id'] = u_id
    session['username'] = name
    session['email'] = email
    session['isAdmin'] = isAdmin

# -------------------------------------------------------

# function for destroying the session variables
def destroySession(): 
    session["u_id"] = None
    session["name"] = None
    session["email"] = None
    session["isAdmin"] = None

# -------------------------------------------------------

if __name__ == '__main__': 
    app.run(debug = True)