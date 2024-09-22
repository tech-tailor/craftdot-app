#!/usr/bin/python3
"""init file"""


from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()