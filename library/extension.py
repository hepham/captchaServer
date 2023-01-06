from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
db = SQLAlchemy()
ma = Marshmallow()
