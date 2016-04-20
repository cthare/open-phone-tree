# Open Phone Tree
# cthare

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
from contextlib import closing
import twilio.twiml


# application start
app = Flask(__name__, instance_path="/instance/")
app.config.from_pyfile('instance/config.py')

# connect to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# initiate database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode="r") as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

# main page
@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

# entry handler
@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',
				  [request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

# logout function
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

# Test directory template
@app.route('/directory', methods=['GET', 'POST'])
def directory():
	if not session.get('logged_in'):
		abort(401)
	#cur = g.db.execute('select title, text from entries order by id desc')
	#entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('directory.html')

# Test directory template
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
	if not session.get('logged_in'):
		abort(401)
	#cur = g.db.execute('select title, text from entries order by id desc')
	#entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('add_menu.html')

# Test directory template
@app.route('/add_number', methods=['GET', 'POST'])
def add_number():
	if not session.get('logged_in'):
		abort(401)
	#cur = g.db.execute('select title, text from entries order by id desc')
	#entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('add_number.html')

# Pseudo-code phone listen
# @app.route('/listen/<menu>', methods=['GET', 'POST'])
# def menu_listen(menu):
# 	resp = twilio.twiml.Response()
	
# 	with resp.gather(numDigits=1, action="/handle-menu", method="POST") as g:
# 		if menu[x] == 'voice':
# 			g.play(menu.url)
# 		else:
# 			g.say(menu.robo)

# 	return str(resp)

# Pseudo-code phone handler
# @app.route('/handler/<menu>', methods=['GET', 'POST'])
# def handle_menu(menu):
# 	digit_pressed = request.values.get('Digits', None)
# 	resp = twilio.twiml.Response()
# 	if digit_pressed not in menu:
# 		return redirect('/wrong-entry')
# 	elif menu[digit_pressed].type == "phoneNumber":
# 		resp.dial(menu[digit_pressed].number)
# 		return resp
# 	else:
# 		redirect('/listen/' + menu[digit_pressed].menuId)

if __name__ == '__main__':
	app.run()