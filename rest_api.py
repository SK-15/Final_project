from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with
from validation import BusinessValidationError, NotFoundError
from model import *
from flask import jsonify
from plotify import logs_plot
import time

api = Api()

user_parser = reqparse.RequestParser()
user_parser.add_argument('name',type=str)
user_parser.add_argument('email',type=str)

tracker_parser = reqparse.RequestParser()
tracker_parser.add_argument('name')
tracker_parser.add_argument('description')
tracker_parser.add_argument('type')
tracker_parser.add_argument('values')

log_parser = reqparse.RequestParser()
log_parser.add_argument('note')
log_parser.add_argument('value')

add_log_parser = reqparse.RequestParser()
add_log_parser.add_argument('log_list')

get_tracker_parser = reqparse.RequestParser()
get_tracker_parser.add_argument('tracker_list')




resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'email': fields.String
}

tracker_resourceField = {
    'id' : fields.String,
    'user_id' : fields.String,
    'name' : fields.String,
    'type' : fields.String,
    'value_types' : fields.String,
    'description' : fields.String
}

class UserAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = user_parser.parse_args()
        name = args["name"]
        email = args["email"]
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise NotFoundError(status_code=404)
        if user.name != name:
            raise BusinessValidationError(status_code=400, error_code="BE1005", error_message="Username does not match email")
        return user
     

    @marshal_with(resource_fields)
    def post(self):
        args = user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)

        if username is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="username is required")

        if email is None:
            raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="email is required")

        if "@" in email:
            pass
        else:
            raise BusinessValidationError(status_code=400, error_code="BE1003", error_message="Invalid email")

        user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()
        if user:
            raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Duplicate user")            

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return None, 200     

class TrackerAPI(Resource):        
    def get(self,id):
        args = get_tracker_parser.parse_args()
        retrn = args['tracker_list']
        if retrn == "0":
            trackers = Tracker.query.filter_by(user_id=id).all()
            return jsonify([Tracker.serialize(tracker) for tracker in trackers])
        else:
            tracker = Tracker.query.filter_by(id=id).first()
            return jsonify(Tracker.serialize(tracker))

    def post(self,id):
        args = tracker_parser.parse_args()
        name = args["name"]
        description = args["description"]
        type = args["type"]
        values = args["values"]
        new_tracker = Tracker(name=name,value_types=values,type=type,description=description,user_id=id)
        db.session.add(new_tracker)
        db.session.commit()
        return None, 200

    def put(self,id):
        args = tracker_parser.parse_args()
        name = args["name"]
        description = args["description"]
        tracker = Tracker.query.filter_by(id=id).first()
        tracker.name = name
        tracker.description = description
        db.session.commit()
        return {'user_id':tracker.user_id}, 200

    def delete(self,id):
        tracker = Tracker.query.filter_by(id=id).first()
        user_id = tracker.user_id
        db.session.delete(tracker)
        db.session.commit()
        return {'user_id': user_id}, 200
        

class LogsAPI(Resource):        
    def get(self,id):
        args = add_log_parser.parse_args()
        rtrn_type = args['log_list']
        #return { 'value' : rtrn_type}
        if rtrn_type == "0":
            logs = Logs.query.filter_by(tracker_id=id).all()
            tracker = Tracker.query.filter_by(id=id).first()
            logs_plot(tracker.type, logs)
            return jsonify([Logs.serialize(log) for log in logs])
        if rtrn_type == "1":
            tracker = Tracker.query.filter_by(id=id).first()
            return jsonify(Tracker.serialize(tracker))
        if rtrn_type == "2":
            log = Logs.query.filter_by(id=id).first()
            return jsonify(Logs.serialize(log))


    def post(self,id):
        tracker = Tracker.query.filter_by(id=id).first()
        args = log_parser.parse_args()
        note = args['note']
        value = args['value']
        time_stamp = time.ctime()
        new_log = Logs(tracker_id=id,user_id=tracker.user_id,value=value,time_stamp=time_stamp,note=note,type=tracker.type)
        db.session.add(new_log)
        db.session.commit()
        return jsonify(Logs.serialize(new_log))

    def put(self,id):
        args = log_parser.parse_args()
        note = args['note']
        value = args['value']
        time_stamp = time.ctime()
        log = Logs.query.filter_by(id=id).first()
        log.note = note
        log.value = value
        log.time_stamp = time_stamp
        db.session.commit()
        return {'trackerid':log.tracker_id}, 200

    def delete(self,id):
        log = Logs.query.filter_by(id=id).first()
        tracker_id = log.tracker_id
        db.session.delete(log)
        db.session.commit()
        return {'trackerid':tracker_id}, 200




api.add_resource(UserAPI, "/api/user")
api.add_resource(TrackerAPI, "/api/tracker/<string:id>")
api.add_resource(LogsAPI, "/api/logs/<string:id>")
