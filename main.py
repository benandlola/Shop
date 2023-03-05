from flask import Flask, session, render_template, redirect, url_for, request
import sqlite3
from datetime import timedelta

app = Flask('app')
app.secret_key = "lolaandben"
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/', methods=['GET', 'POST'])
def home():
  conn = sqlite3.connect("myDatabase.db")
  conn.row_factory = sqlite3.Row
  session['page'] = ['', ''] #set

  #checking out
  if request.method == 'POST':
    cart = session['cart']
    for item in cart:
      cursor = conn.execute("UPDATE products SET stock = ? WHERE product_id = ?", (item['stock']-1, item['product_id']))
      conn.commit()

    session['username'] = None
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

@app.route('/cart', methods=['GET','POST'])
def cart():
    if request.method == 'POST':
      
      conn = sqlite3.connect("myDatabase.db")
      conn.row_factory = sqlite3.Row
      
      rem = request.form.get('remove')
      add = request.form.get('add')
      
      #Add to the cart
      if add:
        cursor = conn.execute("SELECT * FROM products WHERE product_id = ?", (add,))
        product = cursor.fetchone()
        cursor = conn.execute("UPDATE products SET stock = ? WHERE product_id = ?", (product['stock']-1, add,))
        conn.commit()
        cart = session['cart']    
        cart.append(dict(product))
        session['cart'] = cart

        print(session)
        print(session['page'])
        #return to specific category
        if session['page'][0] == 'category':
          print('2')
          sc = session['page'][1]
          cursor = conn.execute("SELECT * FROM products WHERE part_of = ?", (sc,))
          products = cursor.fetchall()
          return render_template('products.html', products=products)
        
        #return to specific item
        elif session['page'][0] == 'search':
          print('3')
          si = session['page'][1]
          cursor = conn.execute("SELECT * FROM products WHERE name LIKE ?", (si,))
          products = cursor.fetchall()
          return render_template('products.html', products=products)
        

        ######
        else: 
          print('4')
          return redirect(url_for('products'))

      #Delete the cart
      if rem == 'all':
        session['cart'] = []
        redirect('/products')

      #If removing one item
      cart = session['cart']
      for item in cart:
        if item['product_id'] == int(rem):
          cursor = conn.execute("SELECT * FROM products WHERE product_id = ?", (rem,))
          product = cursor.fetchone()
          cursor = conn.execute("UPDATE products SET stock = ? WHERE product_id = ?", (product['stock']+1, rem,))
          conn.commit()
          cart.remove(item)
          session['cart'] = cart
          return render_template('cart.html')
    
    return render_template('cart.html')

app.run(host='0.0.0.0', port=8080)