from flask import current_app as app
from flask import render_template, redirect
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import random
#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/travel')
def travel():
    return render_template('travel.html')
