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
        # db.session.remove()
        # db.drop_all()
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
    @unittest.skip
    def test_create_car(self):
        for i in range(30):
            car = CarInOut(
                id = str(uuid.uuid4()),
                park_id = random.choice(
                    [
                        '97a6966a-f402-411e-822d-f0fcbb57fecc',
                     ]
                ),
                plate_no = newplate(),
                in_time = randomDate('2019-11-22 00:00:00', '2019-11-23 00:00:00'),
                in_port = random.choice([1, 3, 5]),
                park_state = 0
            )
            db.session.add(car)
            db.session.commit()

    # 创建角色
    @unittest.skip
    def test_create_role(self):
        role = SysRole(
            id = str(uuid.uuid4()),
            name = '停车场商家',
            state = 1,
        )
        db.session.add(role)
        db.session.commit()

    # 创建用户
    # @unittest.skip
    # def test_create_user(self):
    #     user = SysUser(
    #         id = str(uuid.uuid4()),
    #         nick_name = '测试场',
    #         login_name = 'park2019@test',
    #         state = 1,
    #     )
    #     user.password = 'a'
    #     role = SysRole.query.get('11c60a2b-0561-4f9a-980d-caefcd63c659')
    #     user.roles.append(role)
    #     db.session.add(user)
    #     db.session.commit()
    @unittest.skip
    def test_remove_user_park(self):
        park = ParkInfo.query.get('3ac89fc4-3b5d-4063-8206-d3404cf36dbd')
        print(park)
        users = park.sysuser
        for u in users:
            park.sysuser.remove(u)
            db.session.commit()
    # 获取用户停车场
    @unittest.skip
    def test_parks(self):
        parks = ParkInfo.query.join(sys_user_park).join(SysUser).filter(
            SysUser.id == '5f3030d6-3138-42bb-95a1-9c4979336d2b'
        )
        # print(parks)
        for i in parks:
            print(i.id)

    # 获取用户停车场过车信息
    # @unittest.skip
    def test_cars(self):
        parks = ParkInfo.query.join(sys_user_park).join(SysUser).filter(
            SysUser.id == '5f3030d6-3138-42bb-95a1-9c4979336d2b'
        )
        list = []
        for i in parks:
            print(i.id)
            list.append(i.id)
        # print(list)
        cars = CarInOut.query.filter(CarInOut.park_id.in_(list))
        # cars = CarInOut.query.join(ParkInfo).join(sys_user_park).join(SysUser.id == '5f3030d6-3138-42bb-95a1-9c4979336d2b')
        print(cars)
        for c in cars:
            print(c)

if __name__ == '__main__':
    unittest.main()