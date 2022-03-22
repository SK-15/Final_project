from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from flask import make_response, render_template
from validation import BusinessValidationError, NotFoundError
from model import User, db
from flask import current_app as app
import werkzeug
from flask import abort

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('email')

resource_fields = {
    'user_id':   fields.Integer,
    'username':    fields.String,
    'email':    fields.String
}


class UserAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, username):
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            raise NotFoundError(status_code=404)
        return make_response(render_template('index.html'))

    @marshal_with(resource_fields)
    def put(self, username):
        args = update_user_parser.parse_args()
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

        user = db.session.query(User).filter((User.email == email)).first()
        if email:
            raise BusinessValidationError(status_code=400, error_code="BE1006", error_message="Duplicate email")

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return {'hello': 'world'}        

    @marshal_with(resource_fields)
    def post(self):
        args = create_user_parser.parse_args()
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
        return new_user                

    def delete(self, username):
        user = db.session.query(User).filter(User.username == username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            raise NotFoundError(status=404)

        return "", 200