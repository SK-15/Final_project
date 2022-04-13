from flask import Flask, render_template, request, redirect, session
import os
import time
from model import *
from plotify import logs_plot

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "quant.sqlite3")
db.init_app(app)

@app.route("/",methods=["GET", "POST"])
def login_dashboard():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.name == name:
                user_id = str(user.id)
                return redirect("/user/"+user_id+"/tracker")
            else:
                return "User not found"
        else:
            return "User not found"
    return render_template('index.html')

@app.route("/user/create", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            return "Email Already exists"
        name = request.form['name']
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register_user.html')

@app.route("/user/<string:user_id>/tracker", methods=["GET", "POST"])
def tracker_dashboard(user_id):
    tracker = Tracker.query.filter_by(user_id=user_id).all()
    return render_template("tracker.html", tracker=tracker, n=len(tracker), user_id=user_id)

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
        new_user = Tracker(name=name,value_types=value,type=t_type,description=description,user_id=user_id)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/user/"+user_id+"/tracker")
    return render_template('add_tracker.html', user_id=user_id)

@app.route("/tracker/<string:tracker_id>/delete",methods=["GET","POST"])
def tracker_delete(tracker_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    log = Logs.query.filter_by(tracker_id=tracker_id).first()
    if log:
        return "Please delete all the logs for this tracker first"
    else:
        user_id = str(tracker.user_id)
        db.session.delete(tracker)
        db.session.commit()
        return redirect("/user/"+user_id+"/tracker")


@app.route("/tracker/<string:tracker_id>/update", methods=["GET", "POST"])
def tracker_update(tracker_id):
    if request.method == "POST":
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        user_id = str(tracker.user_id)
        tracker.name = request.form["name"]
        tracker.description = request.form["description"]
        db.session.commit()
        return redirect("/user/"+user_id+"/tracker")
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    return render_template('tracker_update.html', tracker=tracker, tracker_id=tracker_id)


@app.route("/tracker/<string:tracker_id>/log",methods=["GET", "POST"])
def tracker_logs(tracker_id):
    logs = Logs.query.filter_by(tracker_id=tracker_id).all()
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    logs_plot(tracker.type, logs)
    return render_template("logs.html", logs=logs, n=len(logs), tracker_id=tracker_id, user_id=tracker.user_id)


@app.route("/tracker/<string:tracker_id>/log_create", methods=["GET", "POST"])
def add_log(tracker_id):
    if request.method == "POST":
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        user_id = tracker.user_id
        if tracker.type == '1':
            value = request.form['ID']
        else:
            value = request.form['value']
        time_stamp = time.ctime()
        note = request.form['note']
        new_log = Logs(user_id=user_id, tracker_id=tracker_id, value=value, time_stamp=time_stamp, note=note)
        db.session.add(new_log)
        db.session.commit()
        return redirect("/tracker/"+tracker_id+"/log")
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    if tracker.type == '0':
        return render_template("add_log.html", tracker_id=tracker_id)
    else:
        val = tracker.value_types
        val = val.upper()
        values = val.split(',')
        return render_template("add_log_cat.html", tracker_id=tracker_id, values=values)

@app.route("/log/<string:log_id>/delete",methods=["GET","POST"])
def log_delete(log_id):
    log = Logs.query.filter_by(id=log_id).first()
    tracker_id = str(log.tracker_id)
    db.session.delete(log)
    db.session.commit()
    return redirect("/tracker/"+tracker_id+"/log")

@app.route("/log/<string:log_id>/update", methods=["GET", "POST"])
def log_update(log_id):
    if request.method == "POST":
        log = Logs.query.filter_by(id=log_id).first()
        tracker = Tracker.query.filter_by(id=log.tracker_id).first()
        tracker_id = str(log.tracker_id)
        log.note = request.form["note"]
        if tracker.type == '1':
            log.value = request.form['ID']
        else:
            log.value = request.form['value']
        db.session.commit()
        return redirect("/tracker/"+tracker_id+"/log")
    log = Logs.query.filter_by(id=log_id).first()
    tracker = Tracker.query.filter_by(id=log.tracker_id).first()
    if tracker.type == '0':
        return render_template("log_update.html", log=log, log_id=log_id)
    else:
        val = tracker.value_types
        val = val.upper()
        values = val.split(',')
        return render_template('log_update_cat.html', values=values, log=log, log_id=log_id)


if __name__ == '__main__':
    app.debug = True
    app.run()