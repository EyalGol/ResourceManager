from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_simple import JWTManager
import datetime


from user_resources import Auth
from device_resources import Device, DeviceList

import config


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
    app.config['JWT_EXPIRES'] = datetime.timedelta(days=1)
    jwt = JWTManager(app)

    # Place holder for the front end
    @app.route('/')
    def index():
        return render_template('index.html')

    api.add_resource(Device, '/device/<device_id>')
    api.add_resource(DeviceList, '/devices')
    api.add_resource(Auth, '/auth')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.DEBUG)
