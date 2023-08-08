from flask import Flask, url_for, request, redirect, flash, session
from flask.templating import render_template
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from database import *
import hashlib
import base64

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

@app.route('/store', methods=["GET", "POST"])
def store(): 
    categories = getCategories()
    categoryIDs = getCategoryID()
    allItems = getAllItemsFromDB()
    for category in categories: 
        for item in allItems[category]:
            data = base64.b64encode(item[5])
            item[5] = data.decode()
    
    if request.method == "POST": 
        op = request.form["op"]
        p_id = request.form["p_id"]
        updateCart(p_id, op)

    return render_template('store.html', categories = categories, categoryIDs = categoryIDs, allItems = allItems, session = session)
# -------------------------------------------------------

def updateCart(p_id, action): 
    for key in session['cart'].keys(): 
        if key == int(p_id): 
            if action == "plus":
                session['cart'][key] += 1
            if action == "minus": 
                if session['cart'][key] <= 1: 
                    session['cart'][key] = 0
                else:
                    session['cart'][key] -= 1
    print(session['cart'])

# -------------------------------------------------------

@app.route('/cart', methods=["GET", "POST"])
def cart(): 
    allItems = getAllItemsFromDB()
    display_cart = recalculateDisplayCart(session['cart'])
    
    if request.method == "POST": 
        op = request.form["op"]
        cart_id = request.form["cart_id"]
        updateCart(cart_id, op)
        display_cart = recalculateDisplayCart(session['cart'])

    return render_template('cart.html', display_cart = display_cart, session = session)

# -------------------------------------------------------

@app.route('/checkout', methods=["GET", "POST"])
def checkout(): 
    msgColor = ""
    msgText = ""
    display_cart = recalculateDisplayCart(session['cart'])
    total = []
    total.append(calcTotal(display_cart))
    total.append(calcGST(total[0]))
    total.append(calcGST(total[0]))
    total.append(total[0] + (total[1] * 2))

    if request.method == "POST": 
        fullName = request.form["fullname"]
        email = request.form["email"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        zip = request.form["zip"]
        cardName = request.form["card-name"]
        cardNo = request.form["card-no"]
        cardExp = request.form["card-exp"]
        cardCVV = request.form["card-cvv"]

        msg = checkoutPurchase(fullName, email, address, city, state, zip, cardName, cardNo, cardExp, cardCVV, session['cart'])
        if(msg): 
            msgColor = "green"
            msgText = "Checkout Successful!" 
        else: 
            msgColor = "red"
            msgText = "Couldn't checkout, try again!"
    
    return render_template('checkout.html', display_cart = display_cart, total = total, msgColor = msgColor, msg = msgText, session = session)

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
        if(msg == None): 
            msgColor = "green"
            msgText = "New Item Created!"
            getAllItemsFromDB()

        else: 
            msgColor = "red"
            msgText = "Failed to create item, try again!"
    
    return render_template('addItem.html', msgColor = msgColor, msg = msgText, categories = categories, categoryIDs = categoryIDs, session = session)

# -------------------------------------------------------

@app.route('/edit-item', methods=["GET", "POST"])
def editItem(): 
    msgColor = ""
    msgText = ""
    msg = ""
    categories = getCategories()
    categoryIDs = getCategoryID()
    allItems = getAllItemNamesAndIDs()

    if request.method == 'POST': 
        p_id = request.form["p_id"]
        new_name = request.form["new_name"]
        c_id = request.form["c_id"]
        p_qty = request.form["p_qty"]
        p_price = request.form["p_price"]
        p_stock_qty = request.form["p_stock_qty"]

        productDetails = getProductFromID(p_id)
        if c_id == None: 
            c_id = productDetails[6]
        
        if p_qty == None:
            p_qty = productDetails[2]

        if p_stock_qty == None:
            p_stock_qty = productDetails[4]
        
        if p_price == None: 
            p_price = productDetails[3]

        msg = editItemDetails(c_id, p_id, new_name, p_qty, p_price, p_stock_qty)
        if(msg == None): 
            msgColor = "green"
            msgText = "Product Details updated successfully!"

        else: 
            msgColor = "red"
            msgText = "Couldn't edit Product Details!"
    return render_template('editItem.html', msgColor = msgColor, msg = msgText, categories = categories, allItems = allItems, categoryIDs = categoryIDs, session = session)

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
    if request.method == "POST": 
        c_name = request.form["c_name"]
        msg = addNewCategory(c_name)    
        if(msg == None): 
            msgColor = "green"
            msgText = "New Category created!"
            getAllItemsFromDB()

        else: 
            msgColor = "red"
            msgText = "Couldn't create new Category!"
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

# function for setting the session variables
def setSession(u_id, name, email, isAdmin): 
    session['u_id'] = u_id
    session['username'] = name
    session['email'] = email
    session['isAdmin'] = isAdmin
    session['cart'] = initializeCart()

# -------------------------------------------------------

# function for destroying the session variables
def destroySession(): 
    session["u_id"] = None
    session["name"] = None
    session["email"] = None
    session["isAdmin"] = None
    session["cart"] = {}

# -------------------------------------------------------

if __name__ == '__main__': 
    app.run(debug = True)