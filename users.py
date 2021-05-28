from flask_ldap3_login import LDAP3LoginManager
from flask_restful import Resource
from flask import request

import config

ldap_manager = LDAP3LoginManager()
ldap_manager.init_config(config.LDAP_CONFIG)


class Login(Resource):
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        params = request.get_json()
        username = params.get('username', None)
        password = params.get('password', None)

        if not username:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}) 400

            if not self._authenticate:
                return {"msg": "Bad username or password"}, 401

        # Identity can be any data that is json serializable
        ret = {'jwt': create_jwt(identity=username)}
        return jsonify(ret), 200

    def authenticate(username, password):
        """
        Authenticates a user
        :return: True if authentication passed
        """
        if config.AUTH == 'NO-AUTH':
            return True
        elif config.AUTH == 'LDAP':
            return ldap_manager.authenticate(username, password).status
        else:
            return False
