from flask import request, jsonify
from flask.views import MethodView
from passlib.hash import bcrypt

from pygmy.model import UserManager, LinkManager
from pygmy.validator.user import UserSchema
from pygmy.validator.link import LinkSchema, ValidationError
from pygmy.app.auth import APITokenAuth, TokenAuth
from pygmy.core.logger import log


class UserApi(MethodView):
    """Signup and get user info"""
    schema = UserSchema()

    def get(self, user_id=None):
        params = dict()
        if user_id is not None:
            user = UserManager().get(user_id)
        elif request.args.get('email'):
            params['email'] = request.args.get('email')
            user = UserManager().find(**params)
        if user is None:
            return jsonify(dict(error="User not found")), 404
        result = self.schema.dump(user)
        return jsonify(result), 200

    def post(self):
        manager = UserManager()
        payload = request.get_json()
        try:
            data = self.schema.load(payload)
        except ValidationError as errors:
            log.error('Error in the request payload %s', errors)
            err_msg = errors.messages_dict
            return jsonify(err_msg), 400

        if manager.find(email=data['email']):
            return jsonify(dict(error='User exists')), 400
        user = manager.add(**data)
        result = self.schema.dump(user)
        tokens = TokenAuth().create_token(
            identity=payload.get('email'))
        result.update(tokens)
        return jsonify(result), 201


class Auth(MethodView):
    """User login class."""
    schema = UserSchema()

    def post(self):
        params = request.get_json()
        email = params.get('email')
        password = params.get('password')
        if not email:
            return jsonify(dict(error="Email muss angegeben werden.")), 400
        if not password:
            return jsonify(dict(error="Passwort muss angegeben werden.")), 400

        user = UserManager().find(email=email)
        if user is None:
            return jsonify(dict(
                error='Kein Benutzer gefunden mit folgender Email: {}'.format(email))), 404
        if email != user.email or not bcrypt.verify(password, user.password):
            return jsonify(dict(error="Ungültige Email oder Passwort.")), 400
        result = self.schema.dump(user)
        tokens = TokenAuth().create_token(identity=email)
        result.update(tokens)
        return jsonify(result), 200


@APITokenAuth.token_required()
def get_links(user_id=None):
    """Get all links that belong to user `user_id`"""

    manager = LinkManager()
    schema = LinkSchema()
    if request.method == 'GET':
        user_email = APITokenAuth.get_jwt_identity()
        if not user_email:
            return jsonify(dict(error='Ungültiges/Abgelaufenes token')), 400
        user = UserManager().get_by_email(email=user_email)
        if not user:
            return jsonify(dict(error='Ungültiges/Abgelaufenes token')), 400
        links = manager.get_by_owner(owner_id=user.id)
        if not links:
            return jsonify([]), 200
        result = schema.dump(links, many=True)
        return jsonify(result)
