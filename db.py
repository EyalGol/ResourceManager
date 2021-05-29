import sqlite3
import typing
from jsons import JsonSerializable

import config


class Singleton(type):
    """
    Singleton metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SQLWrapper(metaclass=Singleton):
    """
    Wraps sqlite as a singleton for ease of use
    """

    def __init__(self, path: str = config.DB_PATH):
        """
        :param path: Path to the db file
        """
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.con.cursor()

    def exec(self, *args, **kwargs):
        return self.cur.execute(*args, **kwargs)

    def commit(self) -> None:
        self.con.commit()


# associated table
# create table devices (device_id text primary key, is_acquired bool, release_time int,  used_by text, used_for text)
class Device(JsonSerializable):
    def __init__(self, device_id: str, is_acquired: bool = False, release_time: int = 0, used_by: str = '',
                 used_for: str = ''):
        """
        :param device_id: device id
        :param is_acquired: is the device acquired
        :param release_time: timestamp - when the until when the device is acquired
        :param used_by: username of the user who acquired the device
        :param used_for: description of the use of the device
        """
        self.used_for = used_for
        self.used_by = used_by
        self.release_time = release_time
        self.is_acquired = is_acquired
        self.device_id = device_id

    def __repr__(self):
        return f'(\'{self.device_id}\', {self.is_acquired}, {self.release_time}, \'{self.used_by}\', \'{self.used_for}\')'


class DeviceDB:
    TABLE_NAME = 'devices'

    def __init__(self, db=SQLWrapper()):
        self.db = db

    def get_all_devices(self) -> typing.List[Device]:
        """
        All devices
        """
        response = self.db.exec(f'select * from {self.TABLE_NAME}')
        return [Device(*device) for device in response]

    def get_device(self, device_id: str) -> Device:
        """
        Get device by id
        :return: Device or None if there is no such device
        """
        response = self.db.exec(f'select * from {self.TABLE_NAME} where device_id = \'{device_id}\'')
        device = response.fetchone()
        if device:
            return Device(*device)
        return None

    def acquire_device(self, device_id: str, username: str, release_time: int, used_for: str = ''):
        """
        Acquire a device by device id
        :param device_id: device id
        :param username: Username of the acquirer
        :param release_time: release timestamp
        :param used_for: description of the device use
        :raises: RuntimeError
        """
        device = self.get_device(device_id)
        if device.is_acquired:
            raise RuntimeError('Device already acquired')

        self.db.exec(
            f'update {self.TABLE_NAME} set is_acquired = true, used_by = \'{username}\', release_time = {release_time},'
            f' used_for = \'{used_for}\' where device_id = \'{device_id}\'')
        self.db.commit()

    def release_device(self, device_id: str, username: str):
        """
        Release device by device id
        :param username: username TODO: check privileges
        :param device_id: device id
        """
        device = self.get_device(device_id)
        if not device.is_acquired:
            return

        self.db.exec(
            f'update {self.TABLE_NAME} set is_acquired = false, used_by = \'\', release_time = 0, used_for = \'\''
            f' where device_id = \'{device_id}\'')
        self.db.commit()
