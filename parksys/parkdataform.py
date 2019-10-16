# -*- coding : utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

class ParkDataForm(FlaskForm):
    inputName = StringField(
        # '停车场名称',
        validators=[DataRequired("请输入停车场名称"), Length(2, 20)],
        render_kw={
            'id': "inputName",
            'class': 'form-control',
        }
    )
    inputContact = StringField(
        # '联系人',
        validators=[Length(0, 10)],
        render_kw={
            'id': 'inputContact',
            'class': 'form-control',
        }
    )
    inputMobile = IntegerField(
        # '联系电话',
        render_kw={
            'id': 'inputContact',
            'class': 'form-control',
        }
    )
    inputAddress = StringField(
        # '地址',
        validators=[DataRequired('请输入停车场地址'), Length(3, 50)],
        render_kw={
            'id': 'inputAddress',
            'class': 'form-control',
        }
    )
    inputLongitude = DecimalField(
        # '经度',
        render_kw={
            'id': 'inputLongitude',
            'class': 'form-control'
        }
    )
    inputLatitude = DecimalField(
        # '纬度',
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
        render_kw={
            'id': "inputMonthlyParking",
            'class': 'form-control',
        },
        validators=[DataRequired('请输入月卡车位')]
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