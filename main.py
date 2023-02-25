from flask import Flask, session, render_template, redirect, url_for, request
import sqlite3

app = Flask('app')

print('HERE')

conn = sqlite3.connect('myDatabase.db')
cursor = conn.execute('SELECT * FROM products')
prods = cursor.fetchall()

print('ASD')
  
for a in prods:
  print(a)

cursor = conn.execute('SELECT * FROM categories')
cats = cursor.fetchall()

for b in cats:
  print(b)

cursor = conn.execute('SELECT * FROM users')
users = cursor.fetchall()

for c in users:
  print(c)


@app.route('/')
def hello_world():
  return "Let's shop!???"

app.run(host='0.0.0.0', port=8080)