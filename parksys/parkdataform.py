# -*- coding : utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp

class LoginForm(FlaskForm):
    loginname = StringField(
        # 登录名
        validators=[DataRequired("请输入用户名"), Length(min=2, max=50)],
        render_kw={
            'id': 'loginname',
            'type': 'text',
            'class': 'form-control',
            'placeholder': '登录名',
        }
    )
    password = StringField(
        # 密码
        validators=[DataRequired("请输入密码"), Length(min=6, max=32)],
        render_kw={
            'id': 'password',
            'type': 'password',
            'class': 'form-control',
            'placeholder': '密码',
        }
    )

class ParkDataForm(FlaskForm):
    inputName = StringField(
        # '停车场名称',
        validators=[DataRequired("请输入停车场名称"), Length(min=2, max=20)],
        render_kw={
            'id': 'inputName',
            'class': 'form-control',
            'required': 'required',
        }
    )
    inputContact = StringField(
        # '联系人',
        render_kw={
            'id': 'inputContact',
            'class': 'form-control',
        }
    )
    inputMobile = StringField(
        # '联系电话',
        # validators=[Regexp("1[35789]\d{9}", message="手机格式不正确")],
        render_kw={
            'id': 'inputMobile',
            'class': 'form-control',
        }
    )
    inputAddress = StringField(
        # '地址',
        validators=[DataRequired('请输入停车场地址'), Length(3, 50)],
        render_kw={
            'id': 'inputAddress',
            'class': 'form-control',
            'required': 'required',
        }
    )
    inputLongitude = DecimalField(
        # '经度'
        validators=[DataRequired('请正确填写经度')],
        render_kw={
            'id': 'inputLongitude',
            'class': 'form-control'
        }
    )
    inputLatitude = DecimalField(
        # '纬度'
        validators=[DataRequired('请正确填写纬度')],
        render_kw={
            'id': 'inputLatitude',
            'class': 'form-control'
        }
    )
    inputType = SelectField(
        # 停车场类型
        render_kw={
            'class': 'form-control custom-select',
            'id': "inputType",
        },
        coerce=int,
        choices=[(0, '公用'), (1, '私人')]
    )
    inputMonthlyParking = IntegerField(
        validators=[DataRequired('请正确填写月卡数量')],
        render_kw={
            'id': "inputMonthlyParking",
            'class': 'form-control',
        },
    )
    inputChargingRules = TextAreaField(
        render_kw={
            'id': 'inputChargingRules',
            'class': 'form-control',
            'rows': '4'
        }
    )
    inputParkRemarks = TextAreaField(
        render_kw={
            'id': 'inputParkRemarks',
            'class': 'form-control',
            'rows': '3'
        }
    )

    def get_errors(self):
        errors = ''
        for v in self.errors.values():
            for m in v:
                errors += m
            errors += '\n'
        return errors
