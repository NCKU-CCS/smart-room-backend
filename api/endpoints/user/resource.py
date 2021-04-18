import secrets

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from loguru import logger


from utils.oauth import USER_AUTH, g
from .model import User


class UserResource(Resource):
    """User Management"""

    def __init__(self):
        # Create New User
        self._set_post_parser()
        # User Change Password
        self._set_put_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        user_arguments = ["account", "password"]
        for arg in user_arguments:
            self.post_parser.add_argument(
                arg, type=str, required=True, location="json", help=f"Create User: {arg} is required"
            )

    def _set_put_parser(self):
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument(
            "original_password",
            type=str,
            required=True,
            location="json",
            help="Reset password: original_password is required",
        )
        self.put_parser.add_argument(
            "new_password", type=str, required=True, location="json", help="Reset password: new_password is required"
        )

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get User Information: UUID and Name"""
        logger.info(f"[Get User Request]\nUser Account:{g.account}")
        user = User.query.filter_by(uuid=g.uuid).first()
        response = {"uuid": user.uuid, "account": user.account}
        return response

    # pylint: enable=R0201

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def put(self):
        """Change User Password"""
        logger.info(f"[Put User Request]\nUser Account:{g.account}")
        user = User.query.filter_by(uuid=g.uuid).first()
        args = self.put_parser.parse_args()
        if check_password_hash(user.password, args["original_password"]):
            user.password = generate_password_hash(args["new_password"])
            user.token = secrets.token_hex()
            User.update(user)
            return {"message": "Accept", "token": user.token}
        return {"message": "Reject"}, 400

    # pylint: enable=R0201

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def post(self):
        """Add User Account"""
        args = self.post_parser.parse_args()
        user = User.query.filter_by(account=args["account"]).one_or_none()
        if user:
            return {"error": "Account already exists"}, 409
        user = {
            "account": args["account"],
            "password": generate_password_hash(args["password"]),
            "token": secrets.token_hex(),
        }
        if User(**user).add():
            return {"message": "Account created", "token": user["token"]}, 201
        return {"error": "Account Create Failed"}, 400

    # pylint: enable=R0201


class LoginResource(Resource):
    """User Login"""

    def __init__(self):
        # User Login
        self._set_post_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            "account", type=str, required=True, location="json", help="Post Login: account is required"
        )
        self.post_parser.add_argument(
            "password", type=str, required=True, location="json", help="Post Login: password is required"
        )

    # pylint: disable=R0201
    def post(self):
        """Login"""
        args = self.post_parser.parse_args()
        user = User.query.filter_by(account=args["account"]).one_or_none()
        if user:
            if check_password_hash(user.password, args["password"]):
                g.account = user.account
                g.token = user.token
            else:
                logger.warning(f"[Login Failed] Password Incorrect. Account: {args['account']}")
                return {"error": "Account or Password Invalid"}, 401
        else:
            logger.warning(f"[Login Failed] Account Not Fount. Account: {args['account']}")
            return {"error": "Unauthorized Access"}, 401
        logger.info(f"[Login] Account:{g.account}")
        return {"token": user.token}

    # pylint: enable=R0201
