# -*- coding : utf-8 -*-
import os
import config
import unittest
from app import app
from sysunittest.plateno import newplate
from sysunittest.timepicker import randomDate
from parksys.models import *
import uuid
import random


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        # app.config.from_object(config.DevelopmentConfig)
        app.app_context().push()

    def tearDown(self):
        print('ok')

    # 创建停车场
    @unittest.skip
    def test_create_park(self):
        for i in range(2):
            park = ParkInfo(
                id=str(uuid.uuid4()),
                name='二环路的里面%s' % (random.randint(10,100)),
                address='厦门市思明区观日路%s号' % (random.randint(10,100)),
                longitude='118.185422',
                latitude='24.492036',
                type='1',
                create_by='admin',
                state=1,
            )
            db.session.add(park)
            db.session.commit()


    # 创建过车记录
    def test_create_car(self):
        for i in range(30):
            car = CarInOut(
                id = str(uuid.uuid4()),
                park_id = '557711d6-2488-4e85-b706-96ed630fbbad',
                plate_no = newplate(),
                in_time = randomDate('2019-10-01 12:12:12', '2019-11-05 00:00:00'),
                in_port = random.choice([1, 3, 5]),
                park_state = 0
            )
            db.session.add(car)
            db.session.commit()
if __name__ == '__main__':
    unittest.main()