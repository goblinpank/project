import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase



class Weapons(SqlAlchemyBase):
    __tablename__ = 'weapons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    picture = sqlalchemy.Column(sqlalchemy.String)




