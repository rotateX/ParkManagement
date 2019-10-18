# -*- coding : utf-8 -*-
import os
import config
import unittest
from app import app

from parksys.models import *
import uuid


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        # app.config.from_object(config.DevelopmentConfig)
        app.app_context().push()

    def tearDown(self):
        print('ok')

    def test_create_park(self):
        park = ParkInfo(
            id=str(uuid.uuid4()),
            name='xxpark',
            address='厦门市思明区观日路03号',
            longitude='118.185422',
            latitude='24.492036',
            type='1',
            create_by='admin',
            state=0,
        )
        db.session.add(park)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()