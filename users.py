from flask_ldap3_login import LDAP3LoginManager
from flask_restful import Resource
from flask import request
from flask_jwt_simple import create_jwt

import config


class Auth(Resource):
    ldap_manager = LDAP3LoginManager()
    ldap_manager.init_config(config.LDAP_CONFIG)

    def post(self):
        if config.AUTH != 'NO_AUTH':
            if not request.is_json:
                return {"msg": "Missing JSON in request"}, 400

            params = request.get_json()
            username = params.get('username', None)
            password = params.get('password', None)

            if not username:
                return {"msg": "Missing username parameter"}, 400
            if not password:
                return {"msg": "Missing password parameter"}, 400

            if not self._authenticate(username, password):
                return {"msg": "Bad username or password"}, 401

            return {'jwt': create_jwt(identity=username)}

        elif config.AUTH == 'NO_AUTH':
            return {'jwt': create_jwt(identity='NO_AUTH')}

        else:
            return 'Authentication type not set', 500

    def _authenticate(self, username, password):
        """
        Authenticates a user
        :return: True if authentication passed
        """
        if config.AUTH == 'NO_AUTH':
            return True
        elif config.AUTH == 'LDAP':
            return self.ldap_manager.authenticate(username, password).status
        else:
            return False
