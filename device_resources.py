from flask_restful import Resource
from flask import abort, request
from flask_jwt_simple import jwt_required, get_jwt_identity

from db import DeviceDB


class Device(Resource):
    def __init__(self, db=DeviceDB()):
        self.db = db

    def get(self, device_id):
        self._check_if_device_exists(device_id)
        return self.db.get_device(device_id).json

    @jwt_required
    def post(self, device_id):
        self._check_if_device_exists(device_id)
        if not request.is_json:
            return 'Missing request json', 400

        data = request.get_json()
        action = data.get('action', None)
        if not action:
            return 'Missing action parameter', 400

        if action == 'acquire':
            return self._acquire(device_id)
        elif action == 'release':
            return self._release(device_id)
        else:
            return f'Invalid action {action}', 400

    def _check_if_device_exists(self, device_id):
        if not self.db.get_device(device_id):
            abort(400, f'Device: {device_id} does not exist')

    def _acquire(self, device_id):
        data = request.get_json()
        release_time = data.get('release_time', None)
        used_for = data.get('used_for', '')
        if not release_time:
            abort(400, 'Missing release_time parameter')

        try:
            self.db.acquire_device(device_id, get_jwt_identity(), int(release_time), used_for)
        except RuntimeError:
            return f'Acquiring Device {device_id} failed'
        return f'Device {device_id} acquired successfully'

    def _release(self, device_id):
        self.db.release_device(device_id, get_jwt_identity())
        return f'Device {device_id} released successfully'


class DeviceList(Resource):
    def __init__(self, db=DeviceDB()):
        self.db = db

    def get(self):
        return [device.json for device in self.db.get_all_devices()]
