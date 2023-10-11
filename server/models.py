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


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    mission_field = relationship(
        'Mission', back_populates='planet_field', cascade='all, delete, delete-orphan')
    # Add serialization rules
    serialize_rules = ('-mission_field')


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    mission_field = relationship(
        'Mission', back_populates='scientist_field', cascade='all, delete, delete-orphan')
    # Add serialization rules
    serialize_rules = ('-mission_field')
    # Add validation

    @validates('name')
    def validate_name(self, key, value):
        if value:
            return value
        raise ValueError('must have a name')

    @validates('field_of_study')
    def validate_field_of_study(self, key, value):
        if value:
            return value
        raise ValueError('must have a field_of_study')


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    scientist_field = relationship('Scientist', back_populates='mission_field')
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists_table.id'))

    planet_field = relationship('Planet', back_populates='mission_field')
    planet_id = db.Column(db.Integer, db.ForeignKey('planets_table.id'))

    # Add serialization rules
    serialize_rules = ('-planet_field', '-scientist_field')

    # Add validation
    @validates('name')
    def validate_name(self, key, value):
        if value:
            return value
        raise ValueError('must have a name')

    @validates('scientist_id', 'planet_id')
    def validate_id(self, key, value):
        if value:
            return value
        raise ValueError('must have a id')

# add any models you may need.
