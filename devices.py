from flask_restful import Resource
from flask import abort, request

devices = {'1': 1, '2': 2, '3': 3}


class Device(Resource):
    def __init__(self):
        self.devices = devices

    def get(self, device_id):
        self._check_if_device_exists(device_id)
        return self.devices[device_id]

    def post(self, device_id):
        self._check_if_device_exists(device_id)
        data = request.json
        action = data.get('action', None)
        if not action:
            return 'Missing action parameter', 400

        if action == 'acquire':
            return self._acquire(device_id)
        elif action == 'release':
            return self._release(device_id)

    def _check_if_device_exists(self, device_id):
        if device_id not in self.devices:
            abort(400, f'Device: {device_id} does not exist')

    def _acquire(self, device_id):
        return 'acquire'

    def _release(self, device_id):
        return 'release'


class DeviceList(Resource):
    def __init__(self):
        self.devices = devices

    def get(self):
        return self.devices
