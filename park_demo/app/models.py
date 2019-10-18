from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .exceptions import ValidationError


class Permissions(object):
    SELECT = 0x01
    UPLOAD = 0x02
    PARK_ADMIN = 0x04
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {'User': (Permissions.UPLOAD |
                          Permissions.SELECT, True),
                 'PARK_ADMIN': (Permissions.UPLOAD |
                                Permissions.SELECT |
                                Permissions.PARK_ADMIN, False),
                 'Administrator': (0xff, False)
                 }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    park_info = db.relationship('ParkInfo', backref='administrator', lazy='dynamic')

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dump({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    @property
    def password(self):
        raise AttributeError('password 不可以读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class CarInOut(db.Model):
    """
    定义停车场过车信息表
    """
    __tablename__ = 'car_in_out'
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('park_info.id'), comment='停车场外键')
    order_id = db.Column(db.String(64), index=True, unique=True)
    plate_no = db.Column(db.String(64))
    in_time = db.Column(db.DateTime())
    out_time = db.Column(db.DateTime())
    stay_time = db.Column(db.Time())

    @staticmethod
    def from_json(json_post):
        order_id = json_post.get('order_id')
        if order_id is None or order_id == '':
            raise ValidationError('POST中没有车牌或订单号')
        return CarInOut(order_id=order_id)  # 返回实例对象给视图函数

    def to_json(self):
        pass


class ParkInfo(db.Model):
    """
    定义停车场基本信息表
    """
    __tablename__ = 'park_info'
    id = db.Column(db.Integer, primary_key=True, comment='停车场ID')
    name = db.Column(db.String(20), nullable=False, comment='停车场名字')
    administrator_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='停车场管理员用户外键')
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

    def to_json(self):
        pass

    @staticmethod
    def from_json(json_post):
        pass

