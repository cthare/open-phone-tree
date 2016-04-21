import os
from open_phone_tree import app
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
from contextlib import closing

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