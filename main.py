from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
import sqlite3
from datetime import timedelta

'''
A logged in user can also see her order history which should include the list of items purchased and total cost of the order.


A logged in user can see his/her previous order history.
The front end is user friendly: website is easy and intuitive to navigate, no server error messages are presented to to user (if an error occurs, give a user friendly message).
Website style: products have pictures.
'''

#TODO Session Permanence


app = Flask('app')
app.secret_key = "lolaandben"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/', methods=['GET', 'POST'])
def home():
  conn = sqlite3.connect("myDatabase.db")
  conn.row_factory = sqlite3.Row
  session['page'] = ['', ''] #set

  #CHECKOUT
  if request.method == 'POST':
    cart = session['cart']
    for item in cart:
      prod = item['id']
      new_stock = item['stock'] - item['quantity']
      if new_stock < 0:
        error =  str(item['quantity'] - item['stock']) + ' many items of ' + str(item['name']) + ' in cart'
        return render_template('cart.html', error=error)
      conn.execute("UPDATE products SET stock = ? WHERE id = ?",(new_stock, prod,))
      conn.commit()
    conn.commit()

    session['cart'] = []
    return redirect('/')

  cursor = conn.execute("SELECT * FROM products")
  products = cursor.fetchall()
  cursor = conn.execute("SELECT * FROM categories")
  categories = cursor.fetchall()

  return render_template('home.html', products=products, categories=categories)

#Login Page
@app.route('/login', methods=['POST'])
def login():
  if request.method == 'POST':
    name = request.form['username']
    passw = request.form['password']

    conn = sqlite3.connect("myDatabase.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM users")
    users = cursor.fetchall()

    for user in users:
      if name == user['username'] and passw == user['password']:
        session['username'] = name
        session['cart'] = []
      
  return redirect('/')

#Create account Page
@app.route('/create_account', methods=['GET','POST'])
def create_account():
  error = ''
  if request.method == 'POST':
    conn = sqlite3.connect("myDatabase.db")
    conn.row_factory = sqlite3.Row
    name = request.form['username']
    passw = request.form['password']
    fname = request.form['firstname']
    lname = request.form['lastname']

    if name == '':
      error = 'username cannot be empty'
      return render_template('create_account.html', error=error)
    elif passw == '':
      error = 'password cannot be empty'
      return render_template('create_account.html', error=error)
    elif fname == '':
      error = 'firstname cannot be empty'
      return render_template('create_account.html', error=error)
    elif lname == '':
      error = 'lastname cannot be empty'
      return render_template('create_account.html', error=error)
    
    #check if username in use
    cursor = conn.execute('SELECT username FROM users')
    users = cursor.fetchall()
    for user in users:
      if user['username'] == name:
        error = 'username already taken'
        return render_template('create_account.html', error=error)

    conn.execute("INSERT INTO users VALUES (?,?,?,?)", (name, passw, fname, lname))
    conn.commit()
    return redirect('/')
  
  return render_template('create_account.html', error=error)

#Displays products by categories or all
@app.route('/products', methods=['GET','POST'])
def products():
    if request.method == 'POST':
      conn = sqlite3.connect("myDatabase.db")
      conn.row_factory = sqlite3.Row

      cursor = conn.execute("SELECT * FROM products WHERE part_of = ?", (request.form.get('category_select'),))
      products = cursor.fetchall()

      #store for return
      session['page'] = ['category', request.form.get('category_select')]

      return render_template('products.html', products=products)
    
    return redirect('/')
  
#Search for specific product or categories
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
      conn = sqlite3.connect("myDatabase.db")
      conn.row_factory = sqlite3.Row
      search = '%' + request.form.get('search') + '%'
      cursor = conn.execute("SELECT * FROM products WHERE name LIKE ?", (search,))
      products = cursor.fetchall()

      session['page'] = ['search', search]

      return render_template('products.html', products=products)
    
    return redirect('/')

#able to view the Cart and edit
@app.route('/cart', methods=['GET','POST'])
def cart():
    if request.method == 'POST':
      
      conn = sqlite3.connect("myDatabase.db")
      conn.row_factory = sqlite3.Row
      
      rem = request.form.get('remove')
      add = request.form.get('add')
      
      #Add to the cart
      if add:
        cursor = conn.execute("SELECT * FROM products WHERE id = ?", (add,))
        product = cursor.fetchone()
        cart = session['cart']   

        #check to see if already added to update quantity; otherwise create
        seen = False
        for item in cart:
          if item['id'] == product['id']:
            seen = True
            break
        if seen:
          item['quantity'] += 1
        else:
          added = dict(product)
          added['quantity'] = 1
          cart.append(added)
          session['cart'] = cart

        session['cart'] = cart

        #return to specific category
        if session['page'][0] == 'category':
          sc = session['page'][1]
          cursor = conn.execute("SELECT * FROM products WHERE part_of = ?", (sc,))
          products = cursor.fetchall()
          return render_template('products.html', products=products)
        
        #return to specific item
        elif session['page'][0] == 'search':
          si = session['page'][1]
          cursor = conn.execute("SELECT * FROM products WHERE name LIKE ?", (si,))
          products = cursor.fetchall()
          return render_template('products.html', products=products)
        
        else: 
          return redirect(url_for('products'))

      #Delete the cart
      if rem == 'all':
        session['cart'] = []
        redirect('/products')

      #If removing one item
      cart = session['cart']
      for item in cart:
        if item['id'] == int(rem):
          if item['quantity'] > 1:
            item['quantity'] -= 1
          else:
            cart.remove(item)
          session['cart'] = cart
          return render_template('cart.html')
    
    return render_template('cart.html')

app.run(host='0.0.0.0', port=8080)