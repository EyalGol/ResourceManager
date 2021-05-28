from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_simple import JWTManager
from users import Login

from devices import Device, DeviceList

import config


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
    jwt = JWTManager(app)

    # Place holder for the front end
    @app.route('/')
    def index():
        return render_template('index.html')

    api.add_resource(Device, '/device/<device_id>')
    api.add_resource(DeviceList, '/devices')
    api.add_resource(Login, '/login')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.DEBUG)
