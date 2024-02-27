#!/usr/bin/python3
"""
Containsss class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacttts with MySQL databasee"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """querrry on currentt database sessionn"""
        new_dict = {}
        for u in classes:
            if cls is None or cls is classes[u] or cls is u:
                objs = self.__session.query(classes[u]).all()
                for v in objs:
                    key = v.__class__.__name__ + '.' + v.id
                    new_dict[key] = v
        return (new_dict)

    def new(self, v):
        """add  object to current databasre session"""
        self.__session.add(v)

    def save(self):
        """commit changes of the currentt database session"""
        self.__session.commit()

    def delete(self, v=None):
        """delete from the current database session v if not None"""
        if v is not None:
            self.__session.delete(v)

    def reload(self):
        """reloadingg data from database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """callingg remove() method on private session attributeg"""
        self.__session.remove()