import psycopg2
import psycopg2.extras

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

# create_script = '''
#     create table if not exists users (
#         u_id integer not null, 
#         username varchar(100) not null, 
#         gender boolean not null, 
#         email varchar(100) not null, 
#         passcode varchar(200), 
#         isAdmin boolean not null default false, 
#         PRIMARY KEY (u_id)
#     );

#     create table if not exists category (
#         c_id integer not null, 
#         c_name varchar(100) not null, 
#         PRIMARY KEY (c_id)
#     );

#     create table if not exists shop_items (
#         s_id integer not null, 
#         s_name varchar(100) not null, 
#         s_pack_qty varchar(50), 
#         s_price float not null, 
#         s_stock_qty integer not null, 
#         c_id integer not null, 
#         FORIEGN KEY (c_id) REFERENCES category (c_id)
#     );

#     create table if not exists orders (
#         o_id integer not null, 
#         u_id integer not null, 
#         name varchar(100) not null, 
#         email varchar(100) not null, 
#         addr varchar(200) not null, 
#         city varchar(50) not null, 
#         state varchar(50) not null, 
#         zip integer not null, 
#         order_total float not null, 
#         purchase varchar(200) not null, 
#         PRIMARY KEY (o_id), 
#         FORIEGN KEY (u_id) REFERENCES users (u_id)
#     );

#     create sequence if not exists public.user_seq_no
#         increment 1
#         start 1
#         minvalue 1
#         maxvalue 99999
#         owned by users.u_id;

#     alter sequence public.user_seq_no
#         owner to postgres;

#     create sequence if not exists public.category_seq_no
#         increment 1
#         start 1
#         minvalue 1
#         maxvalue 99999
#         owned by category.c_id;

#     alter sequence public.category_seq_no
#         owner to postgres;

#     create sequence if not exists public.order_seq_no
#         increment 1
#         start 1
#         minvalue 1
#         maxvalue 99999
#         owned by booking.booking_id;

#     alter sequence public.order_seq_no
#         owner to postgres;
# '''
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



# -------------------------------------------------------



# -------------------------------------------------------



# -------------------------------------------------------



# -------------------------------------------------------



# -------------------------------------------------------

