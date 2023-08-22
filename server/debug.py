#!/usr/bin/env python3

from app import app
from models import db, Planet, Scientist, Mission

if __name__ == '__main__':
    with app.app_context():

        # s1 = Scientist(name='', field_of_study='test')
        # db.session.add(s1)
        # db.session.commit()

        m1 = Mission(name='test mission', scientist_id=1, planet_id=1)
        db.session.add(m1)
        db.session.commit()
