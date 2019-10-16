# -*- coding : utf-8 -*-

from exts import db
from datetime import datetime
from flask_login import UserMixin


sys_user_park = db.Table(
    'sys_user_park',
    db.Column('park_info_id', db.String(64), db.ForeignKey('park_info.id'), primary_key=True),
    db.Column('sys_user_id', db.String(64), db.ForeignKey('sys_user.id'), primary_key=True)
)


class ParkInfo(db.Model):
    """
    定义停车场基本信息表
    """
    __tablename__ = 'park_info'
    id = db.Column(db.String(64), primary_key=True, comment='停车场ID')
    name = db.Column(db.String(20), nullable=False, comment='停车场名字')
    contact = db.Column(db.String(10), comment='联系人')
    mobile = db.Column(db.String(15), comment='联系电话')
    address = db.Column(db.String(50), nullable=False, comment='停车场地址')
    longitude = db.Column(db.DECIMAL(10, 7), nullable=False, comment='经度')
    latitude = db.Column(db.DECIMAL(10, 7), nullable=False, comment='纬度')
    type = db.Column(db.Integer, nullable=False, comment='停车场类型（0公共，1私人）')
    total_parking_space = db.Column(db.Integer, comment='总车位')
    empty_parking_space = db.Column(db.Integer, comment='空余车位')
    monthly_parking_space = db.Column(db.Integer, comment='月卡车位')
    charging_rules = db.Column(db.String(100), comment='收费规则')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    create_by = db.Column(db.String(20), nullable=False, comment='创建人')
    update_on = db.Column(db.DateTime,  default=datetime.now, onupdate=datetime.now, comment='修改时间')
    update_by = db.Column(db.String(20), comment='修改人')
    delete_on = db.Column(db.DateTime, comment='删除时间')
    delete_by = db.Column(db.String(20), comment='删除人')
    state = db.Column(db.Integer, default=1, comment='状态(0删除，1启用)')
    remarks = db.Column(db.String(50), comment='备注')
    carinout = db.relationship('CarInOut', backref='parkinfo', lazy='dynamic')
    moncategory = db.relationship('MonthlyCategory', backref='parkinfo', lazy='dynamic')
    sysuser = db.relationship('SysUser', secondary=sys_user_park, backref='parkinfo', lazy='dynamic')

    def __repr__(self):
        return 'park_info： id[%s], name[%s], ' % (self.id, self.name)


class CarInOut(db.Model):
    """
    定义过车信息表
    """
    __tablename__ = 'car_in_out'
    id = db.Column(db.String(64), primary_key=True, comment='过车记录ID')
    park_id = db.Column(db.String(64), db.ForeignKey('park_info.id'))
    plate_no = db.Column(db.String(10), nullable=False, comment='车牌')
    in_time = db.Column(db.DateTime, comment='进场时间')
    out_time = db.Column(db.DateTime, comment='出场时间')
    in_port = db.Column(db.String(20), comment='进场通道')
    out_port = db.Column(db.String(20), comment='出场通道')
    in_man = db.Column(db.String(20), comment='进场管理员')
    out_man = db.Column(db.String(20), comment='出场管理员')
    stay_min = db.Column(db.Integer, comment='停留分钟')
    fee_require = db.Column(db.DECIMAL(7, 2), comment='应收金额')
    fee_receipt = db.Column(db.DECIMAL(7, 2), comment='实收金额')
    pay_type = db.Column(db.Integer, comment='支付方式（0现金，1微信，2支付宝，3代付，4优惠券）')
    park_state = db.Column(db.Integer, comment='停车状态(0停车中，1停车结束，2异常停车)')
    remarks = db.Column(db.String(50), comment='备注')
    parkingpay = db.relationship('ParkingPay', backref='carinout', lazy='dynamic')

    def __repr__(self):
        return 'car_in_out: id[%s] - parkname[%s] - plate_no[%s] - in_time[%s] - out_time[%s]' % (
            self.id, self.park_id, self.plate_no, self.in_time, self.out_time
        )


class ParkingPay(db.Model):
    """
    定义临停缴费表
    """
    __tablename__ = 'parking_pay'
    id = db.Column(db.String(64), primary_key=True, comment='订单ID')
    car_id = db.Column(db.String(64), db.ForeignKey('car_in_out.id'))
    order_id = db.Column(db.String(64), comment='订单号')
    mchorder_id = db.Column(db.String(64), comment='商户订单号')
    fee_require = db.Column(db.DECIMAL(7, 2), comment='应收金额')
    fee_receipt = db.Column(db.DECIMAL(7, 2), comment='实收金额')
    fee_free = db.Column(db.DECIMAL(7, 2), comment='优惠金额')
    pay_type = db.Column(db.Integer, comment='支付方式（1微信，2支付宝）')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    pay_on = db.Column(db.DateTime, comment='支付时间')
    state = db.Column(db.Integer, comment='支付状态（0待支付，1支付完成，2关闭支付）')
    remarks = db.Column(db.String(50), comment='备注')

    def __repr__(self):
        return 'parking_pay: id[%s] - car_id[%s] - 订单号[%s] - 应收[%s] - 实收[%s] - 支付类型[%s] - 状态[%s] ' % (
            self.id, self.car_id, self.order_id, self.fee_require, self.fee_receipt, self.pay_type, self.state
        )


class MonthlyCategory(db.Model):
    """
    定义月卡分类表
    """
    __tablename__ = 'monthly_category'
    id = db.Column(db.String(64), primary_key=True, comment='月卡分类ID')
    park_id = db.Column(db.String(64), db.ForeignKey('park_info.id'))
    name = db.Column(db.String(20), nullable=False, comment='月卡名称')
    price = db.Column(db.DECIMAL(7, 2), nullable=False, comment='月卡单价')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    create_by = db.Column(db.String(20), comment='创建人')
    update_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    update_by = db.Column(db.String(20), comment='修改人')
    delete_on = db.Column(db.DateTime, comment='删除时间')
    delete_by = db.Column(db.String(20), comment='删除人')
    state = db.Column(db.Integer, comment='状态（0删除，1启用）')
    monapply = db.relationship('MonthlyApply', backref='monthly_category', lazy='dynamic')

    def __repr__(self):
        return 'monthly_category: id[%s] - park_id[%s] - 月卡名称[%s] - 单价[%s] - 状态[%s]' % (
            self.id, self.park_id, self.name, self.money, self.state
        )


class MonthlyApply(db.Model):
    """
    定义月卡申请表
    """
    __tablename__ = 'monthly_apply'
    id = db.Column(db.String(64), primary_key=True, comment='月卡申请ID')
    category_id = db.Column(db.String(64), db.ForeignKey('monthly_category.id'))
    plate_no = db.Column(db.String(1000), nullable=False, comment='月卡车牌')
    begin_date = db.Column(db.Date, nullable=False, comment='开始日期')
    end_date = db.Column(db.Date, nullable=False, comment='结束日期')
    price = db.Column(db.DECIMAL(7, 2), nullable=False, comment='月卡单价')
    applicant = db.Column(db.String(10), comment='联系人')
    mobile = db.Column(db.String(15), comment='联系电话')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    create_by = db.Column(db.String(20), comment='创建人')
    update_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    update_by = db.Column(db.String(20), comment='修改人')
    delete_on = db.Column(db.DateTime, comment='删除时间')
    delete_by = db.Column(db.String(20), comment='删除人')
    state = db.Column(db.Integer, comment='状态（0删除，1启用，2过期）')
    remarks = db.Column(db.String(50), comment='备注')
    monpay = db.relationship('MonthlyPay', backref='monthly_apply', lazy='dynamic')

    def __repr__(self):
        return 'monthly_apply: id[%s] - category_id[%s] - 车牌[%s] - 开始时间[%s] - 结束时间[%s] - 状态[%s]' % (
            self.id, self.category_id, self.plate_no, self.begin_date, self.end_date, self.state
        )

    def get_monpay(self):
        pass


class MonthlyPay(db.Model):
    """
    月卡缴费表
    """
    __tablename__ = 'monthly_pay'
    id = db.Column(db.String(64), primary_key=True, comment='月卡订单ID')
    apply_id = db.Column(db.String(64), db.ForeignKey('monthly_apply.id'))
    order_id = db.Column(db.String(64), comment='订单号')
    mchorder_id = db.Column(db.String(64), comment='商户订单号')
    months = db.Column(db.Integer, comment='缴费时长')
    fee_require = db.Column(db.DECIMAL(7, 2), comment='应收金额')
    fee_receipt = db.Column(db.DECIMAL(7, 2), comment='实收金额')
    fee_free = db.Column(db.DECIMAL(7, 2), comment='优惠金额')
    pay_type = db.Column(db.Integer, comment='缴费方式（1微信，2支付宝）')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    pay_on = db.Column(db.DateTime, comment='支付时间')
    state = db.Column(db.Integer, comment='支付状态（0待支付，1支付完成，2关闭支付）')

    def __repr__(self):
        return 'monthly_pay: id[%s] - apply_id[%s] - order_id[%s] - 缴费时长[%s] - 实收[%s] - 支付状态[%s]' % (
            self.id, self.apply_id, self.order_id, self.months, self.fee_receipt, self.state
        )


class SysRole(db.Model):
    """
    定义角色表
    """
    __tablename__ = 'sys_role'
    id = db.Column(db.String(64), primary_key=True, comment='角色ID')
    name = db.Column(db.String(20), comment='角色名称')
    permission = db.Column(db.Integer, comment='权限值')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    delete_on = db.Column(db.DateTime, comment='删除时间')
    state = db.Column(db.Integer, comment='状态（0删除，1启用）')
    sysuser = db.relationship('SysUser', backref='sys_role', lazy='dynamic')

    def __repr__(self):
        return 'sys_role: id[%s] - name[%s] - permission[%s] - state[%s]' % (
            self.id, self.name, self.permission, self.state
        )


class SysUser(db.Model):
    """
    定义平台管理员信息表
    """
    __tablename__ = 'sys_user'
    id = db.Column(db.String(64), primary_key=True, comment='管理员ID')
    role_id = db.Column(db.String(64), db.ForeignKey('sys_role.id'))
    nick_name = db.Column(db.String(20), comment='昵称')
    login_name = db.Column(db.String(20), unique=True, comment='登录名')
    password = db.Column(db.String(64), comment='密码')
    create_on = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    create_by = db.Column(db.String(20), comment='创建人')
    update_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    update_by = db.Column(db.String(20), comment='修改人')
    delete_on = db.Column(db.DateTime, comment='删除时间')
    delete_by = db.Column(db.String(20), comment='删除人')
    state = db.Column(db.Integer, comment='状态（0删除，1启用）')

    def __repr__(self):
        return 'sys_user: id[%s] - role_id[%s] - login_name[%s] -state[%s]' % (
            self.id, self.role_id, self.login_name, self.state
        )
