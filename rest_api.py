from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with
from validation import BusinessValidationError, NotFoundError
from model import *
from flask import jsonify
from plotify import logs_plot

api = Api()

user_parser = reqparse.RequestParser()
user_parser.add_argument('name',type=str)
user_parser.add_argument('email',type=str)

add_tracker_parser = reqparse.RequestParser()
add_tracker_parser.add_argument('name')
add_tracker_parser.add_argument('description')
add_tracker_parser.add_argument('type')
add_tracker_parser.add_argument('values')



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
    def get(self,userid):
        trackers = Tracker.query.filter_by(user_id=userid).all()
        return jsonify([Tracker.serialize(tracker) for tracker in trackers])

    def post(self,userid):
        args = add_tracker_parser.parse_args()
        name = args.get("name",None)
        description = args.get("description",None)
        type = args.get("type",None)
        values = args.get("values",None)
        new_tracker = Tracker(name=name,value_types=values,type=type,description=description,user_id=userid)
        db.session.add(new_tracker)
        db.session.commit()
        return None, 200

    def put(self,trackerid):
        args = add_tracker_parser.parse_args()
        name = args.get("name",None)
        description = args.get("description",None)
        tracker = Tracker.query.filter_by(id=trackerid).first()
        tracker.name = name
        tracker.description = description
        db.session.commit()
        return {'user_id':tracker.user_id}, 200

    def delete(self,trackerid):
        tracker = Tracker.query.filter_by(id=trackerid).first()
        user_id = tracker.user_id
        db.session.delete(tracker)
        db.session.commit()
        return {'user_id': user_id}, 200
        

class LogsAPI(Resource):        
    def get(self,trackerid):
        logs = Logs.query.filter_by(tracker_id=trackerid).all()
        tracker = Tracker.query.filter_by(id=trackerid).first()
        logs_plot(tracker.type, logs)
        return jsonify([Logs.serialize(log) for log in logs])

    def post(self,trackerid):
        pass

    def put(self,logid):
        pass

    def delete():
        pass




api.add_resource(UserAPI, "/api/user")
api.add_resource(TrackerAPI, "/api/tracker/<string:userid>","/api/tracker/<string:trackerid>")
api.add_resource(LogsAPI, "/api/logs/<string:trackerid>","/api/logs/<string:logid>")
