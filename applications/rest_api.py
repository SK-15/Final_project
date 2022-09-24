from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with
from applications.validation import BusinessValidationError, NotFoundError,SchemaValidationError
from applications.model import User, Tracker, Logs
from applications.database import db
from flask import jsonify
from applications.plotify import logs_plot
import time
import werkzeug
from webargs import fields
from webargs.flaskparser import use_args

api = Api()

class UserAPI(Resource):
    @use_args({"name": fields.Str(required=True),"email": fields.Str(required=True)}, location="query")
    def get(self,args):
        name = args['name']
        email = args["email"]
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise NotFoundError(status_code=404, error_code="NT1001",error_message="username is required")
        if user.name != name:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="Username does not match email")
        return {'name': user.name, 'email': user.email, 'id': user.id} ,200
        
     

    @use_args({"name": fields.Str(required=True),"email": fields.Str(required=True)}, location="query")
    def post(self,args):
        username = args['name']
        email = args['name']

        if username is None:
            raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="username is required")

        if email is None:
            raise BusinessValidationError(status_code=400, error_code="BE1003", error_message="email is required")

        if "@" in email:
            pass
        else:
            raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Invalid email")

        user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()
        if user:
            raise BusinessValidationError(status_code=400, error_code="BE1005", error_message="Duplicate user")            

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return None, 200     

class TrackerAPI(Resource): 
    @use_args({"tracker_list": fields.Str(required=True),"id": fields.Str(required=True)}, location="query")       
    def get(self,args):
        retrn = args['tracker_list']
        userid = args['id']
        if retrn == "0":
            trackers = Tracker.query.filter_by(user_id=userid).all()
            return jsonify([Tracker.serialize(tracker) for tracker in trackers])
        else:
            tracker = Tracker.query.filter_by(id=userid).first()
            return jsonify(Tracker.serialize(tracker))


    @use_args({"name": fields.Str(required=True),"type": fields.Str(required=True),"description": fields.Str(required=True),"values": fields.Str(required=True),"id": fields.Str(required=True)}, location="query")
    def post(self,args):
        name = args["name"]
        description = args["description"]
        type_t = args["type"]
        values = args["values"]
        userid = args['id']
        new_tracker = Tracker(name=name,value_types=values,type=type_t,description=description,user_id=userid)
        db.session.add(new_tracker)
        db.session.commit()
        return None, 200

    @use_args({"name": fields.Str(required=True),"description": fields.Str(required=True) ,"id": fields.Str(required=True)}, location="query")
    def put(self,args):
        name = args["name"]
        description = args["description"]
        trackerid = args['id']
        tracker = Tracker.query.filter_by(id=trackerid).first()
        tracker.name = name
        tracker.description = description
        db.session.commit()
        return {'user_id':tracker.user_id}, 200

    @use_args({"id": fields.Str(required=True)}, location="query")
    def delete(self,args):
        trackerid = args['id']
        tracker = Tracker.query.filter_by(id=trackerid).first()
        log = Logs.query.filter_by(tracker_id=trackerid).first()
        if log:
            raise BusinessValidationError(status_code=400, error_code="BE1006", error_message="Logs are present please delete all the logs for this tracker")
        user_id = tracker.user_id
        db.session.delete(tracker)
        db.session.commit()
        return {'user_id': user_id}, 200
        

class LogsAPI(Resource):      
    @use_args({"log_list": fields.Str(required=True),"id": fields.Str(required=True)}, location="query")
    def get(self,args):
        rtrn_type = args['log_list']
        trackerid = args['id']
        if rtrn_type == "0":
            logs = Logs.query.filter_by(tracker_id=trackerid).all()
            tracker = Tracker.query.filter_by(id=trackerid).first()
            logs_plot(tracker.type, logs)
            return jsonify([Logs.serialize(log) for log in logs])
        if rtrn_type == "1":
            tracker = Tracker.query.filter_by(id=trackerid).first()
            return jsonify(Tracker.serialize(tracker))
        if rtrn_type == "2":
            log = Logs.query.filter_by(id=trackerid).first()
            return jsonify(Logs.serialize(log))

    @use_args({"note": fields.Str(required=True),"value": fields.Str(required=True), "id": fields.Str(required=True)}, location="query")
    def post(self,args):
        trackerid = args['id']
        tracker = Tracker.query.filter_by(id=trackerid).first()
        note = args['note']
        value = args['value']
        time_stamp = time.ctime()
        new_log = Logs(tracker_id=trackerid,user_id=tracker.user_id,value=value,time_stamp=time_stamp,note=note,type=tracker.type)
        db.session.add(new_log)
        db.session.commit()
        return jsonify(Logs.serialize(new_log))

    @use_args({"note": fields.Str(required=True),"value": fields.Str(required=True), "id": fields.Str(required=True)}, location="query")
    def put(self,args):
        logid = args['id']
        note = args['note']
        value = args['value']
        time_stamp = time.ctime()
        log = Logs.query.filter_by(id=logid).first()
        log.note = note
        log.value = value
        log.time_stamp = time_stamp
        db.session.commit()
        return {'trackerid':log.tracker_id}, 200

    @use_args({"id": fields.Str(required=True)}, location="query")
    def delete(self,args):
        logid = args['id']
        log = Logs.query.filter_by(id=logid).first()
        tracker_id = log.tracker_id
        db.session.delete(log)
        db.session.commit()
        return {'trackerid':tracker_id}, 200

api.add_resource(UserAPI, "/api/user")
api.add_resource(TrackerAPI, "/api/tracker")
api.add_resource(LogsAPI, "/api/logs")