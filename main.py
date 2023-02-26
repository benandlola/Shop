from flask import Flask, session, render_template, redirect, url_for, request
import sqlite3

app = Flask('app')
app.secret_key = "lolaandben"

@app.route('/', methods=['GET', 'POST'])
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
        session['password'] = passw

        #products
        cursor = conn.execute("SELECT * FROM products")
        products = cursor.fetchall()

        #categories
        cursor = conn.execute("SELECT * FROM categories")
        categories = cursor.fetchall()

        return render_template('home.html', products=products, categories=categories)
      
    #if not a user
    return redirect('/')

  return render_template('login.html')

  
#Displays products by categories or all
@app.route('/products', methods=['POST'])
def products():
    if request.method == 'POST':
      selected = request.form.get('category_select')

      conn = sqlite3.connect("myDatabase.db")
      conn.row_factory = sqlite3.Row

      if selected == 'All':
        cursor = conn.execute("SELECT * FROM products")
      else:
        cursor = conn.execute("SELECT * FROM products WHERE part_of = ?", (selected,))
      products = cursor.fetchall()

      return render_template('products.html', products=products, selected=selected)
    
    return redirect('/')
  

@app.route('/home', methods=['GET', 'POST'])
def home():
  if 'username' in session:
    return render_template('home.html')

app.run(host='0.0.0.0', port=8080)