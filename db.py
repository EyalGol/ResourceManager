import sqlite3

import config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SQLWrapper(metaclass=Singleton):
    """
    Wraps sqlite as a singleton for ease of use
    """
    def __init__(self, path=config.DB_PATH):
        con = sqlite3.connect(path)
        self.cur = con.cursor()

    def execute(self, *args, **kwargs):
        return self.cur.execute(*args, **kwargs)
