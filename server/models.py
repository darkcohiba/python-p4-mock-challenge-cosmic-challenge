from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Scientist(db.Model, SerializerMixin):
    __tablename__='scientist_table'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    field_of_study=db.Column(db.String, nullable=False)

    mission_s_relationship=db.relationship('Mission', back_populates='scientist_field', cascade="all, delete")

class Planet(db.Model, SerializerMixin):
    __tablename__='planet_table'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    nearest_star= db.Column(db.String)
    distance_from_earth= db.Column(db.Integer)

    mission_p_relationship=db.relationship('Mission', back_populates='planet_field', cascade="all, delete")


class Mission(db.Model, SerializerMixin):
    __tablename__='mission_table'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    scientist_id=db.Column(db.Integer, db.ForeignKey('scientist_table.id'), nullable=False)
    scientist_field=db.relationship('Scientist', back_populates='mission_s_relationship')

    planet_id=db.Column(db.Integer, db.ForeignKey('planet_table.id'), nullable=False)
    planet_field=db.relationship('Planet', back_populates='mission_p_relationship')

    serialize_rules=('-scientist_field','-planet_field.mission_p_relationship')






