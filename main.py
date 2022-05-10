from flask import Flask, render_template, jsonify
from flask import request, redirect, session
import os
import time
from model import db, Tracker
from plotify import logs_plot
import requests
from rest_api import api


current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "quant.sqlite3")
db.init_app(app)
api.init_app(app)

@app.route("/",methods=["GET", "POST"])
def login_dashboard():
    if request.method == "POST":
        data = { 'name' : request.form['name'], 'email' : request.form['email'] }
        response = requests.get('http://127.0.0.1:5000/api/user',params = data)
        response = response.json()
        userid = response['id']
        return redirect("/user/"+userid+"/tracker")
    return render_template('index.html')

@app.route("/user/create", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        data = {'name':name,'email':email}
        response = requests.post('http://127.0.0.1:5000/api/user',data = data)
        response = response.json()
        return redirect('/')
    return render_template('register_user.html')

@app.route("/user/<string:user_id>/tracker", methods=["GET", "POST"])
def tracker_dashboard(user_id):
    response = requests.get('http://127.0.0.1:5000/api/tracker/'+user_id)
    response = response.json()
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
        data = {'name':name,'description':description,'type':t_type,'values':value}
        response = requests.post('http://127.0.0.1:5000/api/tracker'+user_id,data = data)
        response = response.json()
        return redirect("/user/"+user_id+"/tracker")
    return render_template('add_tracker.html', user_id=user_id)

@app.route("/tracker/<string:tracker_id>/delete",methods=["GET","POST"])
def tracker_delete(tracker_id):
    response = requests.delete('http://127.0.0.1:5000/api/tracker'+tracker_id)
    response = response.json()
    user_id = response['user_id']
    return redirect("/user/"+user_id+"/tracker")


@app.route("/tracker/<string:tracker_id>/update", methods=["GET", "POST"])
def tracker_update(tracker_id):
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        data = {'name':name,'description':description}
        response = requests.put('http://127.0.0.1:5000/api/tracker'+tracker_id,data = data)
        response = response.json()
        user_id = response['user_id']
        return redirect("/user/"+user_id+"/tracker")
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    return render_template('tracker_update.html', tracker=tracker, tracker_id=tracker_id)


@app.route("/tracker/<string:tracker_id>/log",methods=["GET", "POST"])
def tracker_logs(tracker_id):
    response = requests.get('http://127.0.0.1:5000/api/logs/'+tracker_id,params = {'log_list':0})
    response = response.json()
    logs = []
    for rep in response:
        logs.append(rep)
    return render_template("logs.html", logs=logs, n=len(logs))


@app.route("/tracker/<string:tracker_id>/log_create", methods=["GET", "POST"])
def add_log(tracker_id):
    if request.method == "POST":
        value = request.form['log_value']
        note = request.form['note']
        data = {'note ':note,'value':value}
        response = requests.post('http://127.0.0.1:5000/api/logs/'+tracker_id,data=data)
        response = response.json()
        return redirect("/tracker/"+tracker_id+"/log",logs = response)
    response = requests.get('http://127.0.0.1:5000/api/logs/'+tracker_id,params = {'log_list':1})
    response = response.json()
    return render_template("add_log.html", tracker = response,tracker_id = tracker_id)

@app.route("/log/<string:log_id>/delete",methods=["GET","POST"])
def log_delete(log_id):
    response = requests.delete('http://127.0.0.1:5000/api/logs/'+log_id)
    response = response.json()
    tracker_id = response['trackerid']
    return redirect("/tracker/"+tracker_id+"/log")

@app.route("/log/<string:log_id>/update", methods=["GET", "POST"])
def log_update(log_id):
    if request.method == "POST":
        note = request.form['note']
        value = request.form['log_value']
        data = {'note':note, 'value':value}
        response = requests.put('http://127.0.0.1:5000/api/logs/'+tracker_id,data=data)
        response = response.json()
        tracker_id = response['trackerid']
        return redirect("/tracker/"+tracker_id+"/log")
    response = requests.get('http://127.0.0.1:5000/api/logs/'+log_id,params = {'log_list':2})
    response = response.json()
    return render_template('log_update.html',log = response)


if __name__ == '__main__':
    app.debug = True
    app.run()