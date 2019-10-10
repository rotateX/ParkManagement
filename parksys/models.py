# -*- coding : utf-8 -*-

from exts import db


class ParkInfo(db.Model):
    """
    定义停车场基本信息表
    """
    __tablename__ = 'park_info'
    id = db.Column(db.String(64), primary_key=True, comment='停车场ID')
    name = db.Column(db.String(20), nullable=False, comment='停车场名字')
    contact = db.Column(db.String(10), comment='联系人')
    mobile = db.Column(db.String(15), comment='联系电话')
    address = db.Column(db.String(20), nullable=False, comment='停车场地址')
    longitude = db.Column(db.DECIMAL(10, 7), nullable=False, comment='经度')
    latitude = db.Column(db.DECIMAL(10, 7), nullable=False, comment='纬度')
    type = db.Column(db.Integer, nullable=False, comment='停车场类型')
    total_parking_space = db.Column(db.Integer, comment='总车位')
    empty_parking_space = db.Column(db.Integer, comment='空余车位')
    monthly_parking_space = db.Column(db.Integer, comment='月卡车位')
    charging_rules = db.Column(db.String(100), comment='收费规则')
    create_on = db.Column(db.DateTime,)
