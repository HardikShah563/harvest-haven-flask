import psycopg2
import psycopg2.extras
import base64

hostname = 'localhost'
database = 'harvesthaven'
username = 'postgres'
pwd = 'Hardikts@563'
port_id = 5432

conn = None
cur = None

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

allProductsInTheStore = {}


create_script = '''
    -- USERS TABLE --
    create table if not exists users (
        u_id integer not null, 
        username varchar(100) not null, 
        gender boolean not null, 
        email varchar(100) not null, 
        passcode varchar(200), 
        isAdmin boolean not null default false, 
        PRIMARY KEY (u_id)
    );

    -- CATEGORY TABLE --
    create table if not exists category (
        c_id integer not null, 
        c_name varchar(100) not null, 
        PRIMARY KEY (c_id)
    );

    -- PRODUCTS TABLE --
    create table if not exists products (
        p_id integer not null, 
        p_name varchar(100) not null, 
        p_qty varchar(50) not null, 
        p_price float not null, 
        p_stock_qty integer not null, 
        p_img bytea not null, 
        c_id integer not null, 
        PRIMARY KEY (p_id), 
        FOREIGN KEY (c_id) REFERENCES category (c_id)
    );

    -- ORDERS TABLE --
    create table if not exists orders (
        o_id integer not null, 
        u_id integer not null, 
        username varchar(100) not null, 
        email varchar(100) not null, 
        addr varchar(200) not null, 
        city varchar(50) not null, 
        state_province_ut varchar(50) not null, 
        zip integer not null, 
        order_total float not null, 
        purchase jsonb not null, 
        PRIMARY KEY (o_id), 
        FOREIGN KEY (u_id) REFERENCES users (u_id)
    );

    -- USER_SEQ_NO SEQUENCE --
    create sequence if not exists public.user_seq_no
        increment 1
        start 1
        minvalue 1
        maxvalue 99999
        owned by users.u_id;

    alter sequence public.user_seq_no
        owner to postgres;

    -- CATEGORY_SEQ_NO SEQUENCE --
    create sequence if not exists public.category_seq_no
        increment 1
        start 1
        minvalue 1
        maxvalue 99999
        owned by category.c_id;

    alter sequence public.category_seq_no
        owner to postgres;

    -- PRODUCT_SEQ_NO SEQUENCE --
    create sequence if not exists public.product_seq_no
        increment 1
        start 1
        minvalue 1
        maxvalue 99999
        owned by products.p_id;

    alter sequence public.product_seq_no
        owner to postgres;

    -- ORDER_SEQ_NO SEQUENCE --
    create sequence if not exists public.order_seq_no
        increment 1
        start 1
        minvalue 1
        maxvalue 99999
        owned by booking.booking_id;

    alter sequence public.order_seq_no
        owner to postgres;
'''
# # gender - true is male and false is female
# # card details wont be save therefore did not make columns for that
# cur.execute(create_script)
# conn.commit()

# -------------------------------------------------------

def registerAccount(name, gender, email, password): 
    insert_script = '''
        select email from users where email = %s
    '''
    insert_values = ([email])
    cur.execute(insert_script, insert_values)
    conn.commit()
    if(cur.fetchall()):
        return False

    insert_script = '''
        insert into users (u_id, username, gender, email, passcode) 
        values (NEXTVAL('user_seq_no'), %s, %s, %s, %s)
    '''
    insert_values = (name, gender, email, password)
    cur.execute(insert_script, insert_values)
    if(conn.commit()): 
       return True

# -------------------------------------------------------

def loginAccount(email, password): 
    insert_script = '''
        select passcode from users where email = %s
    '''
    insert_values = ([email])
    cur.execute(insert_script, insert_values)
    conn.commit()
    data = cur.fetchall()
    if(not data):
        return False
    if(data[0][0] == password): 
        return True
    else: 
        return False

# -------------------------------------------------------

def getUID(email): 
    insert_script = '''
        select u_id from users where email = %s
    '''
    insert_values = ([email])
    cur.execute(insert_script, insert_values)
    conn.commit()
    data = cur.fetchone()
    return data[0]

# -------------------------------------------------------

def getName(email): 
    insert_script = '''
        select username from users where email = %s
    '''
    insert_values = ([email])
    cur.execute(insert_script, insert_values)
    conn.commit()
    data = cur.fetchone()
    return data[0]

# -------------------------------------------------------

def adminCheck(email): 
    insert_script = '''
        select isadmin from users where email = %s
    '''
    insert_values = ([email])
    cur.execute(insert_script, insert_values)
    conn.commit()
    data = cur.fetchone()
    return data[0]

# -------------------------------------------------------

def getCategories(): 
    get_script = '''
        select c_name from category
    '''
    cur.execute(get_script)
    conn.commit()
    data = cur.fetchall()
    categories = []
    for category in data: 
        categories.append(category[0])
    return categories
 
# -------------------------------------------------------

def getCategoryID(): 
    get_script = '''
        select c_id from category
    '''
    cur.execute(get_script)
    conn.commit()
    data = cur.fetchall()
    categoryIDs = []
    for id in data: 
        categoryIDs.append(id[0])
    return categoryIDs

# -------------------------------------------------------

def getCategoryById(c_id): 
    get_script = '''
        select c_name from category where c_id = %s
    '''
    get_values = ([c_id])
    cur.execute(get_script, get_values)
    conn.commit()
    data = cur.fetchall()
    return data[0]

# -------------------------------------------------------

def getCategoryIdFromName(c_name): 
    get_script = '''
        select c_id from category where c_name = %s
    '''
    get_values = ([c_name])
    cur.execute(get_script, get_values)
    conn.commit()
    data = cur.fetchall()
    return data

# -------------------------------------------------------

def addNewCategory(c_name):
    add_script = '''
        insert into category
        values (NEXTVAL('category_seq_no'), %s)
    '''
    add_values = ([c_name])
    cur.execute(add_script, add_values)
    if (conn.commit()):
        return True

# -------------------------------------------------------

def editCategoryName(old_id, new_name):
    edit_script = '''
        update category
        set c_name = %s
        where c_id = %s
    '''
    edit_values = (new_name, old_id)
    cur.execute(edit_script, edit_values)
    if (conn.commit()):
        return True

# -------------------------------------------------------

def deleteCategoryCompletely(c_id):
    delete_script = '''
        delete from products where c_id = %s;
        delete from category where c_id = %s;
    '''
    delete_values = (c_id, c_id)
    cur.execute(delete_script, delete_values)
    if (conn.commit()): 
        return True

# -------------------------------------------------------

def getAllItemsFromDB():
    allProductsInTheStore = {}

    categoryList = getCategories()
    for category in categoryList: 
        allProductsInTheStore[category] = []

    get_script = '''
        select * from products
    '''
    cur.execute(get_script)
    conn.commit()
    data = cur.fetchall()

    for product in data: 
        c_name = getCategoryById(product[6])[0]
        allProductsInTheStore[c_name].append(product[:-1])

    return allProductsInTheStore

# -------------------------------------------------------

def getAllItems():
    return allProductsInTheStore

# -------------------------------------------------------

def getAllItemNamesAndIDs(): 
    items = []
    get_script = '''
        select p_id, p_name from products
    '''
    cur.execute(get_script)
    conn.commit()
    data = cur.fetchall()
    return data

# -------------------------------------------------------

def putItems(pName, pQty, pPrice, pStockQty, pImg, cID):     
    insert_script = '''
        insert into products (p_id, p_name, p_qty, p_price, p_stock_qty, p_img, c_id)
        values (NEXTVAL('product_seq_no'), %s, %s, %s, %s, %s, %s)
    '''
    insert_values = (pName, pQty, pPrice, pStockQty, pImg, cID)
    cur.execute(insert_script, insert_values)
    conn.commit()
    get_script = '''
        select * from products where p_name = %s and p_qty = %s
    '''
    get_values = (pName, pQty)
    cur.execute(get_script, get_values)
    if(conn.commit()): 
       return True

# -------------------------------------------------------

def getProductFromID(p_id):
    get_script = '''
        select * from products where p_id = %s
    '''
    get_values = ([p_id])
    cur.execute(get_script, get_values)
    conn.commit()
    data = cur.fetchall()[0]
    return data

# -------------------------------------------------------

def editItemDetails(c_id, p_id, new_name, p_qty, p_price, p_stock_qty):
    edit_script = '''
        update products 
        set p_name = %s, p_qty = %s, p_price = %s, p_stock_qty = %s, c_id = %s where p_id = %s
    '''
    edit_values = (new_name, p_qty, p_price, p_stock_qty, c_id, p_id)
    cur.execute(edit_script, edit_values)
    if (conn.commit()):
        return True

# -------------------------------------------------------

def deleteProduct(p_id):
    delete_script = '''
        delete from products where p_id = %s
    '''
    delete_value = ([p_id])
    cur.execute(delete_script, delete_value)
    if conn.commit(): 
        return True

# -------------------------------------------------------

def initializeCart(): 
    cart = {}
    allItems = getAllItemNamesAndIDs()
    for item in allItems: 
        cart[item[0]] = 0
    return cart

# -------------------------------------------------------

def recalculateDisplayCart(cart):
    display_cart = []
    allItems = getAllItemsFromDB()
    for item in allItems:
        for i in allItems[item]:
            if cart[i[0]] > 0: 
                list = i
                list.append(cart[i[0]])
                data = base64.b64encode(i[5])
                i[5] = data.decode()
                display_cart.append(list)
    return display_cart

# -------------------------------------------------------

def checkoutPurchase(fullName, email, address, city, state, zip, cardName, cardNo, cardExp, cardCVV, cartDict): 
    # creating purchase dict from session['cart']
    purchase = {}
    for item in cartDict:
        print(item)
        if item[1] > 0: 
            purchase[item[0]] = item[1]
    
    # insert_script = ''''''
    # insert_values = ()
    # cur.execute(insert_script, insert_values)
    # if (conn.commit()):
    #     return True

    # CREATE TABLE thetable (
    #     uuid TEXT,
    #     dict JSONB
    # );
    # cur.execute('INSERT into thetable (uuid, dict) values (%s, %s)',
    # ['testName', Json({'id':'122','name':'test','number':'444-444-4444'})])
    return False

# -------------------------------------------------------

def calcTotal(cart): 
    total = 0
    for cart_item in cart: 
        total = total + (cart_item[3] * cart_item[6])
    return total

# -------------------------------------------------------

def calcGST(total):
    return 0.09 * total

# -------------------------------------------------------

def setShopItemsAndCategories():
    getCategories()
    getCategoryID()
    getAllItemsFromDB()
# -------------------------------------------------------

