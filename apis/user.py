import re
from flask_restx import Namespace, Resource, fields
from modules.user import User


api = Namespace('users', description='User related operations')

user_detail = api.model('User detail', {
    'username': fields.String(required=True, description="The account username"),
    'password': fields.String(required=True, description="The account password")
})

user_api_response = api.model('User api response', {
    'success': fields.Boolean(readonly=True, description='The request success or not'),
    'reason': fields.String(readonly=True, description='The reason of response failed'),
})


def check_account_format(username, password):
    if len(username) < 3:
        return False, 'Username is too short'
    if len(username) > 32:
        return False, 'Username is too long'

    if len(password) < 8:
        return False, 'Password is too short'
    if len(password) > 32:
        return False, 'Password is too long'
    if re.search(r"[A-Z]", password) is None:
        return False, 'Password is need one or more uppercase letter'
    if re.search(r"[a-z]", password) is None:
        return False, 'Password is need one or more lowercase letter'
    if re.search(r"[0-9]", password) is None:
        return False, 'Password is need one or more number'

    return True, ''


@api.route('/')
class UserAccount(Resource):
    @api.response("400", "Invalid parameter", user_api_response)
    @api.expect(user_detail)
    @api.marshal_with(user_api_response, code=201)
    def post(self):
        '''
        Create account
        '''
        payload = api.payload
        if "username" not in payload or "password" not in payload:
            return dict(success=False, reason=f"Invalid parameter"), 400

        username, password = payload['username'], payload['password']
        ret, reason = check_account_format(username, password)
        if not ret:
            return dict(success=False, reason=reason), 400
        
        user = User(username, password)
        user.save_db()

        return dict(success=True, reason=f"Create user account success"), 201


@api.route('/verification')
class UserAccountVerification(Resource):
    @api.response("400", "Invalid parameter", user_api_response)
    @api.response("401", "Account verify is failed", user_api_response)
    @api.response("404", "Account is not exist", user_api_response)
    @api.response("429", "Verify too many failed, please try again later", user_api_response)
    @api.expect(user_detail)
    @api.marshal_with(user_api_response, code=200)
    def post(self):
        '''
        Verify account and password
        '''
        payload = api.payload
        if "username" not in payload or "password" not in payload:
            return dict(success=False, reason="Invalid parameter"), 400
        
        username, password = payload['username'], payload['password']
        user = User.get_user(username=username)
        if not user:
            return dict(success=False, reason=f"Account is not exist"), 404

        if user.check_lock():
            return dict(success=False, reason=f"Verify too many failed, please try again later"), 429
 
        success = user.verify(password)
        if success:
            return dict(success=True, reason=f"Account verify is success"), 200
        else:
            return dict(success=False, reason=f"Account verify is failed"), 401
