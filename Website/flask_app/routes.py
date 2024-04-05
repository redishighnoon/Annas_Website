# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, g, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
    if 'email' in session:
        decrypted_email = db.reversibleEncrypt('decrypt', session['email'])
        if isinstance(decrypted_email, bytes):
            decrypted_email = decrypted_email.decode('utf-8')
        return decrypted_email
    else:
        return 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
    form_fields = request.form
    email = form_fields['email']
    password = form_fields['password']

    # Authenticate the user
    auth_result = db.authenticate(email, password)
    if auth_result['success']:
        session.pop('login_attempts', None)  # Reset login attempts counter
        encrypted_email = db.reversibleEncrypt('encrypt', email)
        session['email'] = encrypted_email
        return json.dumps({'success': 1})
    else:
        # Increment login attempts counter
        session['login_attempts'] = session.get('login_attempts', 0) + 1
        return json.dumps({'success': 0, 'error': 'Invalid credentials', 'attempts': session['login_attempts']})

@app.before_request
def decrypt_user_email():
    if 'email' in session:
        decrypted_email = db.reversibleEncrypt('decrypt', session['email'])
        g.decrypted_email = decrypted_email
    else:
        g.decrypted_email = None



#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    emit('status', {
        'msg': getUser() + ' has entered the room.',
        'userId': getUser()
    }, room='main')

@socketio.on('text', namespace='/chat')
def text(message):
    full_user_email = getUser()
    user_identifier = full_user_email.split('@')[0] if '@' in full_user_email else full_user_email
    emit('message', {
        'msg': user_identifier + ': ' + message['msg'], 
        'userId': full_user_email,
    }, room='main')

@socketio.on('left', namespace='/chat')
def left():
    emit('status', {
        'msg': getUser() + ' has left the room.',
        'userId': getUser()
    }, room='main', include_self=False)

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I hold a black belt in taekwondo','I am in the AirForce Reserves','I play games'])
	return render_template('home.html', fun_fact = x)

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	return render_template('resume.html', resume_data = resume_data)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/piano')
def piano():
    return render_template('piano.html')

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    # Extract feedback form data
    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')
    
    # Insert the feedback into the database
    db.insertRows(table='feedback', columns=['name', 'email', 'comment'], parameters=[(name, email, comment)])
    
    # Fetch all feedback for rendering
    all_feedback = db.query("SELECT * FROM feedback")
    
    # Render the feedback page with all feedback entries
    return render_template('processfeedback.html', feedback=all_feedback)
