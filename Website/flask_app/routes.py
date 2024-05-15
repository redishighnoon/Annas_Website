from flask import current_app as app
from flask import render_template, redirect
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import random
#######################################################################################
# MAIN
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

@app.route('/paintings')
def paintings():
    return render_template('paintings.html')

#######################################################################################
# TRAVEL
#######################################################################################
@app.route('/travel')
def travel():
    return render_template('travel.html')

@app.route('/art')
def art():
    return render_template('art.html')

# Routes for the individual cities in Korea
@app.route('/Places_Traveled/Korea/seoul')
def seoul():
    return render_template('Places_Traveled/Korea/seoul.html')

@app.route('/Places_Traveled/Korea/jeju')
def jeju():
    return render_template('Places_Traveled/Korea/jeju.html')

@app.route('/Places_Traveled/korea/busan')
def busan():
    return render_template('Places_Traveled/Korea/busan.html')

@app.route('/Places_Traveled/USA/deathvalley')
def deathvalley():
    return render_template('Places_Traveled/USA/deathvalley.html')

@app.route('/Places_Traveled/USA/washington')
def washington():
    return render_template('Places_Traveled/USA/washington.html')

@app.route('/Places_Traveled/USA/losangeles')
def losangeles():
    return render_template('Places_Traveled/USA/losangeles.html')

@app.route('/Places_Traveled/Iceland/Reykjavik')
def Reykjavik():
    return render_template('Places_Traveled/Iceland/Reykjavik.html')

@app.route('/Places_Traveled/USA/Oahu')
def oahu():
    return render_template('Places_Traveled/USA/oahu.html')

@app.route('/Places_Traveled/Mexico/Guanajuato')
def guanajuato():
    return render_template('Places_Traveled/Mexico/guanajuato.html')

@app.route('/Places_Traveled/USA/Michigan')
def michigan():
    return render_template('Places_Traveled/USA/michigan.html')

@app.route('/Places_Traveled/Philippines/Palawan')
def palawan():
    return render_template('Places_Traveled/Philippines/Palawan/palawan.html')