from flask import render_template, jsonify
from flask import request, redirect, session
from sqlalchemy import null
import requests
from flask import current_app as app

@app.route("/",methods=["GET", "POST"])
def login_dashboard():
    if request.method == "POST":
        data = { 'name' : str(request.form['name']), 'email' : str(request.form['email']) }
        response = requests.get(url = 'http://127.0.0.1:5000/api/user',params=data).json()
        try:
            userid = str(response['id'])
        except KeyError:
            # return response
            return render_template('error.html',message = response)
        # return jsonify(response)
        # email = request.form['email']
        # name = request.form['name']
        # user = User.query.filter_by(email=email).first()
        return redirect('/user/'+userid+'/tracker')
    return render_template('index.html')

@app.route("/user/create", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        data = {'name':str(name),'email':str(email)}
        response = requests.post('http://127.0.0.1:5000/api/user/',params = data)
        response = response.json()
        return redirect('/')
    return render_template('register_user.html')

@app.route("/user/<string:user_id>/tracker", methods=["GET", "POST"])
def tracker_dashboard(user_id):
    response = requests.get('http://127.0.0.1:5000/api/tracker', params={'tracker_list':'0','id':user_id}).json()
    tracker = []
    for rep in response:
        tracker.append(rep)
    return render_template('tracker.html',trackers = tracker, user_id = user_id)


@app.route("/user/<string:user_id>/tracker_create",methods=["GET","POST"])
def tracker_add(user_id):
    if request.method == "POST":
        value='null'
        name = request.form['name']
        description = request.form['description']
        if request.form['ID'] == 'num':
            t_type = '0'  # 0 for numerical type
        if request.form['ID'] == 'mch':
            t_type = '1'  # 1 for multiple choice type
            value = request.form['value']
        data = {'name':name,'description':description,'type':t_type,'values':value,'id':user_id}
        response = requests.post('http://127.0.0.1:5000/api/tracker',params=data).json()
        return redirect("/user/"+user_id+"/tracker")
    return render_template('add_tracker.html', user_id=user_id)

@app.route("/tracker/<string:tracker_id>/delete",methods=["GET","POST"])
def tracker_delete(tracker_id):
    response = requests.delete('http://127.0.0.1:5000/api/tracker',params={'id':tracker_id}).json()
    try:
        userid = str(response['user_id'])
    except KeyError:
        return render_template('error.html',message = response)
    return redirect("/user/"+userid+"/tracker")


@app.route("/tracker/<string:tracker_id>/update", methods=["GET", "POST"])
def tracker_update(tracker_id):
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        data = {'name':name,'description':description,'id':tracker_id}
        response = requests.put('http://127.0.0.1:5000/api/tracker',params = data).json()
        user_id = str(response['user_id'])
        return redirect("/user/"+user_id+"/tracker")
    response = requests.get('http://127.0.0.1:5000/api/tracker', params={'tracker_list':'1','id':tracker_id}).json()
    return render_template('tracker_update.html', tracker=response, tracker_id=tracker_id)


@app.route("/<string:user_id>/<string:tracker_id>/log",methods=["GET", "POST"])
def tracker_logs(user_id,tracker_id):
    response = requests.get('http://127.0.0.1:5000/api/logs',params = {'log_list':'0','id':tracker_id}).json()
    logs = []
    try:
        for rep in response:
            logs.append(rep)
    except:
        pass
    return render_template("logs.html", logs=logs, n=len(logs),user_id = user_id,tracker_id = tracker_id)


@app.route("/<string:user_id>/<string:tracker_id>/log_create", methods=["GET","POST"])
def add_log(user_id,tracker_id):
    if request.method == "POST":
        value = request.form['log_value']
        note = request.form['note']
        data = {'note' : note, 'value' : value, 'id':tracker_id}
        response = requests.post('http://127.0.0.1:5000/api/logs',params=data)
        return redirect("/"+user_id+"/"+tracker_id+"/log")
    response = requests.get('http://127.0.0.1:5000/api/logs',params = {'log_list':'1','id':tracker_id}).json()
    values = null
    try:
        if response['type'] == "1":
            value_types = str(response['value_types'])
            values = value_types.upper()
            values = values.split(',')
    except:
        pass
    return render_template("add_log.html", tracker = response,user_id = user_id,tracker_id = tracker_id,values = values)

@app.route("/<string:user_id>/<string:log_id>/log_delete",methods=["GET","POST"])
def log_delete(user_id,log_id):
    response = requests.delete('http://127.0.0.1:5000/api/logs',params={'id':log_id}).json()
    tracker_id = str(response['trackerid'])
    return redirect("/"+user_id+"/"+tracker_id+"/log")

@app.route("/<string:user_id>/<string:log_id>/log_update", methods=["GET", "POST"])
def log_update(user_id,log_id):
    if request.method == "POST":
        note = request.form['note']
        value = request.form['log_value']
        data = {'note':note, 'value':value, 'id':log_id}
        response = requests.put('http://127.0.0.1:5000/api/logs',params=data).json()
        tracker_id = str(response['trackerid'])
        return redirect("/"+user_id+"/"+tracker_id+"/log")
    response = requests.get('http://127.0.0.1:5000/api/logs',params = {'log_list':'2','id':log_id}).json()
    return render_template('log_update.html',log = response,user_id=user_id)