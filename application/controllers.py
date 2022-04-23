import datetime
import requests
from flask import Flask, jsonify, request, redirect, session
from flask import render_template
from flask_bcrypt import Bcrypt
from flask import current_app as app
from .database import db
from application.models import User, Tracker, TrackerLog
from application.utilities import *

bcrypt = Bcrypt(app) #<-For Password Encryption



### LOGIN PAGE..🚨👮‍♂️🚔👮‍♂️🚓👮‍♂️🚨
@app.route('/login', methods=['GET', 'POST'])
def logIn():
    if request.method=='POST':
        username = request.form.get("username")
        password = request.form.get("pass")

        try:
            # UserAPI GET Request and Response..
            # api_userdata = requests.get(f'http://127.0.0.1:5000/api/user/{username}') 
            api_userdata = requests.get(f'https://qtfself.herokuapp.com/api/user/{username}')
            v1 = api_userdata.status_code
            # api_userdata = api_userdata.content
            # print(api_userdata['username'])
            api_userdata = api_userdata.json()
            # api_userdata = jsonify(api_userdata)
        except:
            return redirect('/login')

        # IF NOT 200 =====>
        if v1 != 200: 
            if v1==500 or v1==404:
                return redirect('/login')
            if v1==400:
                error_code = api_userdata['error_code']
                error_body = api_userdata['error_code']
                if error_code=='USER01':
                    message_head = 'Invalid Input'
                return redirect('/login')
        
        # IF 200 =====>
        #if password matches
        if bcrypt.check_password_hash(api_userdata['password'], password): ###if the password matches
            # start a session and return the HOME PAGE
            username, user_id, user_fname = username, api_userdata['user_id'], api_userdata['fname']
            session['username'] = username
            session['user_id'] = user_id 
            session['user_fname'] = user_fname 
            return redirect('/')
        else: #if the password doesnt match
            return redirect('/login')
    
    ### In case of 'GET' request, if user already login
    if 'username' in session:
        return redirect('/')  #redirect home_page/dashboard 
    
    ### In case of GET request, normally log-in page will be rendered..
    v = render_template('loginPage.html') 
    return v  # return the LogIn Page (Form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('user_fname', None)
    return redirect('/login')


### REGISTER PAGE..✍📝✍📝✍
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        v = render_template('registerPage.html')
        return v
    
    if request.method=='POST':
        username = request.form.get('username')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password = request.form.get('pass')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if usernamevalidation(username) and normalvalidation(fname):
            userobj = User.query.filter_by(username=username).first()
            if userobj: #if the username already exist in record
                return redirect('/register')
            #if the username is unique or not in the database
            # then, register it to the database
            if lname: #if lname given
                if normalvalidation(lname):
                    newuser = User(username=username, fname=fname, lname=lname, password=hashed_password)
                else:
                    return redirect('/register')
            else: #if not
                newuser = User(username=username, fname=fname, password=hashed_password)
            db.session.add(newuser)
            db.session.commit()
            return redirect('/login')
        else:
            return redirect('/register')
    # v = render_template('registerPage.html')
    # return v

@app.route('/contactus')
def contactus():
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    
    v = render_template("contactus.html", userdata=userdata)
    return v

@app.route('/about')
def about():
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    
    v = render_template("about.html", userdata=userdata)
    return v


### HOME PAGE / DASHBOARD...🏡✨🏠✨🏡
@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    
    alltrackers_data = requests.get(f'https://qtfself.herokuapp.com/api/alltrackers/{user_id}')
    v1 = alltrackers_data.status_code
    alltrackers = alltrackers_data.json()

    v = render_template("dashboard.html", userdata=userdata, recordList=alltrackers)
    return v

### CRUD on Tracker Management...

# CREATE NEW TRACKER..
@app.route('/tracker/create', methods=['GET', 'POST'])
def createNewTracker():
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    if request.method=='GET':
        v = render_template("createTracker.html", user_id=user_id, userdata=userdata)
        return v
    
    if request.method=='POST':
        trackername = request.form["trackername"]
        trackerdescr = request.form["trackerdescr"]
        trackertype = request.form["trackertype"]
        trackersettings = request.form["trackersettings"]

        api_response = requests.post(f'https://qtfself.herokuapp.com/api/tracker', json={'user_id':user_id, 'tracker_name':trackername, 'description':trackerdescr, 'track_type':trackertype, 'settings':trackersettings})
        v1 = api_response.status_code
        api_response = api_response.json()
        
        if v1==200 or v1==201:
            pass
        elif v1==409:
            error_head = 'User Not Found'
            error_body = 'Please put correct username or user_id'
            rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
            return rt
        elif v1==400:
            error_code = api_response['error_code']
            error_body = api_response['error_message']
            if error_code=='TRACKER01':
                error_head = 'Invalid Tracker Name'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
            if error_code=='TRACKER02':
                error_head = 'Invalid Tracker Description'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
            if error_code=='TRACKER03':
                error_head = 'Invalid track_type'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
            if error_code=='TRACKER04':
                error_head = '	Invalid settings'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
            if error_code=='TRACKER05':
                error_head = 'Invalid user_id / tracker_id'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
        else:
            error_head = 'Unknown Error'
            error_body = 'Some Unknown Error Occured ! Please Try Again'
            rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)

        return redirect('/')


# DELETE EXISTING TRACKER..
@app.route('/tracker/<int:tracker_id>/delete', methods=['GET', 'POST'])
def deleteExistingTracker(tracker_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')

    if request.method=='GET':
        #get the tracker data from API
        tracker_data = requests.get(f'https://qtfself.herokuapp.com/api/tracker/{tracker_id}')
        v1 = tracker_data.status_code
        tracker_data = tracker_data.json()
        if v1==200 or v1==201:
            pass
        elif v1==404:
            error_head = 'Tracker Not Found'
            error_body = 'Please put correct tracker_id or user_id'
            rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
            return rt
        # elif v1==400:
        #     error_code = tracker_data['error_code']
        #     error_body = tracker_data['error_message']
        #     if error_code=='TRACKER05':
        #         error_head = 'Invalid Tracker Name'
        #         rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
        #         return rt
        else:
            error_head = 'Unknown Error'
            error_body = 'Some Unknown Error Occured ! Please Try Again'
            rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)

        if user_id==tracker_data['user_id']:
            #api delete request
            tracker_data = requests.delete(f'https://qtfself.herokuapp.com/api/tracker/{tracker_id}')
            v1 = tracker_data.status_code
            if v1 != 200:
                error_head = 'Unknown Error'
                error_body = 'Some Unknown Error Occured ! Please Try Again'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
    return redirect('/')


# UPDATE EXISTING TRACKER..
@app.route('/tracker/<int:tracker_id>/update', methods=['GET', 'POST'])
def updateExistingTracker(tracker_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')

    if request.method=='GET':
        #get the tracker data from API
        tracker_data = requests.get(f'https://qtfself.herokuapp.com/api/tracker/{tracker_id}')
        v1 = tracker_data.status_code
        tracker_data = tracker_data.json()
        
        if user_id==tracker_data['user_id']:
            v = render_template("updateTracker.html", trackerobj=tracker_data, userdata=userdata)
            return v
        else:
            error_head = 'Unauthorized Access'
            error_body = 'You do not have permission to check this page'
            rt = render_template("errorPage.html", userdata=userdata, error_head=error_head, error_body=error_body)
            return rt
    
    if request.method=='POST':
        trackername = request.form["trackername"]
        trackerdescr = request.form["trackerdescr"]
        trackertype = request.form["trackertype"]
        trackersettings = request.form["trackersettings"]

        tracker_data = requests.get(f'https://qtfself.herokuapp.com/api/tracker/{tracker_id}')
        tracker_data = tracker_data.json()
        if user_id!=tracker_data['user_id']:
            error_head = 'Unauthorized Access'
            error_body = 'You can not perform this action'
            rt = render_template("errorPage.html", userdata=userdata, error_head=error_head, error_body=error_body)
            return rt

        api_response = requests.put(f'https://qtfself.herokuapp.com//api/tracker/{tracker_id}', data={'tracker_name':trackername, 'description':trackerdescr, 'settings':trackersettings})
        v1 = api_response.status_code
        print("line-5------------")
        api_response = api_response.json()
        if v1==200 or v1==201:
            pass
        elif v1==404:
            error_head = 'Tracker Not Found'
            error_body = 'Please put correct tracker_id or user_id'
            rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
            return rt
        elif v1==400:
            error_code = api_response['error_code']
            error_body = api_response['error_message']
            if error_code=='TRACKER01':
                error_head = 'Invalid Tracker Name'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
            if error_code=='TRACKER02':
                error_head = 'Invalid Tracker Description'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
            if error_code=='TRACKER04':
                error_head = '	Invalid settings'
                rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
                return rt
        else:
            error_head = 'Unknown Error'
            error_body = 'Some Unknown Error Occured ! Please Try Again'
            rt = render_template('errorPage.html', userdata=userdata, error_head=error_head, error_body=error_body)
            return rt

        return redirect('/')


# VIEW DETAILS OF AN EXISTING TRACKER..
@app.route('/tracker/<int:tracker_id>/read', methods=['GET', 'POST'])
def view_aTracker(tracker_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')

    if request.method=='GET':
        trackerdata = requests.get(f'https://qtfself.herokuapp.com/api/tracker/{tracker_id}')
        v1 = trackerdata.status_code
        trackerdata = trackerdata.json()
        
        if user_id!=trackerdata['user_id']:
            error_head = 'Unauthorized Access'
            error_body = 'You do not have permission to check this page'
            rt = render_template("errorPage.html", userdata=userdata, error_head=error_head, error_body=error_body)
            return rt

        loglist = TrackerLog.query.filter_by(user_id=user_id, tracker_id=tracker_id).all()
        lastlog = TrackerLog.query.filter_by(tracker_id=tracker_id,user_id=user_id).order_by(TrackerLog.timestamp.desc()).limit(1).first()
        tname = trackerdata['tracker_name']

        #Function Call For Graph Plotting..
        if loglist:
            if trackerdata['track_type']=='Numerical':
                monthlydata = getmonthlyDatanum(loglist, lastlog, tname)
            else:
                allvars = trackerdata['settings'].split(',')
                monthlydata = getmonthlyDatamcq(loglist, lastlog, tname, allvars)
            
            v = render_template('trackerDetails.html', userdata=userdata,trackerdata=trackerdata, loglist=loglist) #, flag=True)
            return v
        else:
            v = render_template('trackerDetails.html', userdata=userdata,trackerdata=trackerdata, loglist=loglist) #, flag=False)
            return v
    
    return redirect('/')


# CREATE NEW LOG
@app.route('/log/<int:tracker_id>/create', methods=['GET', 'POST'])
def createNewLog(tracker_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    
    if request.method=='GET':
        trackerdata = Tracker.query.get(tracker_id)
        datetimeval = str(datetime.datetime.now())

        if trackerdata.track_type=='Multiple_Choice':
            trackervalues = trackerdata.settings
            tvallist = trackervalues.split(',')
            v = render_template("addNewLog.html", userdata=userdata, trackerdata=trackerdata, dt=datetimeval, tvallist=tvallist)
        else:
            v = render_template("addNewLog.html", userdata=userdata, trackerdata=trackerdata, dt=datetimeval)
        return v
    
    if request.method=='POST':
        timestamp = request.form["timestamp"]
        logvalue = request.form["logvalue"]
        notes = request.form["notes"]

        if logvalue:
            if notes:
                if normalvalidation(notes):
                    newlog = TrackerLog(user_id=user_id, tracker_id=tracker_id, timestamp=timestamp, value=logvalue, note=notes)
                else:
                    v = render_template('invalid_input.html', userdata=userdata)
                    return v
            else:
                newlog = TrackerLog(user_id=user_id, tracker_id=tracker_id, timestamp=timestamp, value=logvalue)
        else:
            v = render_template('invalid_input.html', userdata=userdata)
            return v
        db.session.add(newlog)
        db.session.commit()
        return redirect('/tracker/{tracker_id}/read'.format(tracker_id=tracker_id))


# UPDATE EXISTING LOG
@app.route('/log/<int:log_id>/update', methods=['GET', 'POST'])
def updateExistingLog(log_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    if request.method=='GET':
        logdata = TrackerLog.query.get(log_id)
        trackerdata = Tracker.query.get(logdata.tracker_id)
        timestamp = logdata.timestamp

        if trackerdata.track_type=='Multiple_Choice':
            trackervalues = trackerdata.settings
            tvallist = trackervalues.split(',')
            v = render_template("updateLogEntry.html", userdata=userdata, trackerdata=trackerdata, logdata=logdata, dt=timestamp, tvallist=tvallist)
        else:
            v = render_template("updateLogEntry.html", userdata=userdata, trackerdata=trackerdata, logdata=logdata, dt=timestamp)
        return v
    
    if request.method=='POST':
        update_log = TrackerLog.query.get(log_id)
        tracker_id = update_log.tracker_id
        timestamp = request.form["timestamp"]
        logvalue = request.form["logvalue"]
        notes = request.form["notes"]

        #data update
        update_log.timestamp = timestamp
        update_log.value = logvalue
        if notes:
            # Server Side validation on Notes
            if normalvalidation(notes):
                update_log.note = notes
            else:
                # Show the Invalid Input Error Page
                v = render_template('invalid_input.html', userdata=userdata)
                return v
        db.session.commit()

        return redirect('/tracker/{tracker_id}/read'.format(tracker_id=tracker_id))


# DELETE EXISTING LOG..
@app.route('/log/<int:log_id>/delete', methods=['GET', 'POST'])
def deleteExistingLog(log_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')

    if request.method=='GET':
        #get the log object
        logobj = TrackerLog.query.get(log_id)
        tracker_id = logobj.tracker_id
        #delete the log object
        db.session.delete(logobj)
        db.session.commit()
        
    return redirect('/tracker/{tracker_id}/read'.format(tracker_id=tracker_id))


@app.route('/profile/<int:user_id>')
def profile(user_id):
    try:
        user_id = session['user_id']
        username = session['username']
        fname = session['user_fname']
        userdata = {
            'user_id': user_id,
            'username': username,
            'fname': fname
        }
    except:
        return redirect('/login')
    
    api_userdata = requests.get(f'https://qtfself.herokuapp.com/api/user/{username}')
    v1 = api_userdata.status_code
    api_userdata = api_userdata.json()

    if username!=api_userdata['username']:
        error_head = 'Unauthorized Access'
        error_body = 'You can not perform this action'
        rt = render_template("errorPage.html", userdata=userdata, error_head=error_head, error_body=error_body)
        return rt
    
    v = render_template('profile.html', user_id=user_id, userdata=api_userdata)
    return v

@app.route('/help')
def help():
    v = render_template('help.html')
    return v

