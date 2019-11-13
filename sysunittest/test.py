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

    # def setUp(self):
    #     self.app = app
    #     app.config.from_object(config.DevelopmentConfig)
    #     app.app_context().push()
    #     db.create_all()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    def setUp(self):
        self.app = app
        # app.config.from_object(config.DevelopmentConfig)
        app.app_context().push()
        # db.create_all()

    def tearDown(self):
        print('ok')

    # 创建停车场
    @unittest.skip
    def test_create_park(self):
        for i in range(10):
            park = ParkInfo(
                id=str(uuid.uuid4()),
                name='南山%s号停车场' % (random.randint(10,100)),
                address='致富路%s号' % (random.randint(10,100)),
                longitude='118.185422',
                latitude='24.492036',
                type='1',
                create_by='admin',
                state=1,
            )
            db.session.add(park)
            db.session.commit()


    # 创建过车记录
    # @unittest.skip
    def test_create_car(self):
        for i in range(30):
            car = CarInOut(
                id = str(uuid.uuid4()),
                park_id = random.choice(
                    [
                        'b7fb79e7-78c2-42f8-a238-d62f8748429d',
                        'cbfc83f5-dba8-4e74-b05d-efed3a6661db',
                        '155acbcb-fd0b-4660-90aa-c3f0184a2b87'
                     ]
                ),
                plate_no = newplate(),
                in_time = randomDate('2019-11-13 00:00:00', '2019-11-14 00:00:00'),
                in_port = random.choice([1, 3, 5]),
                park_state = 0
            )
            db.session.add(car)
            db.session.commit()
if __name__ == '__main__':
    unittest.main()