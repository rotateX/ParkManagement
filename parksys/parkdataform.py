# -*- coding : utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, TextAreaField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from parksys.models import *
from  operator import and_

class LoginForm(FlaskForm):
    """
    登录页表单
    """
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
    password = PasswordField(
        # 密码
        validators=[DataRequired("请输入密码"), Length(min=6, max=32)],
        render_kw={
            'id': 'password',
            'type': 'password',
            'class': 'form-control',
            'placeholder': '密码',
        }
    )

class SysUserForm(FlaskForm):
    """
    停车场用户表单
    """
    login_name = StringField(  # 昵称
        validators=[DataRequired("请输入登名"), Length(min=5, max=50)],
        render_kw={
            'id': 'login_name',
            'class': 'form-control',
            'required': 'required',
            'placeholder': '请输入登录名',
        }
    )
    nick_name = StringField(  # 昵称
        validators=[Length(min=2, max=20)],
        render_kw={
            'id': 'nick_name',
            'class': 'form-control',
            'placeholder': '请输入昵称',
        }

    )

    role_type = SelectMultipleField(  # 用户类型
        render_kw={
            "id": "role_type",
            "class": "form-control selectpicker",
            "data-done-button": "true",
            "data-live-search": "true",
            "data-live-search-placeholder": "Search",
            "data-actions-box": "true",
        },
        coerce=str,
    )
    park_relation = SelectMultipleField(  # 关联停车场
        render_kw={
            'id': "park_relation",
            "class": "form-control selectpicker",
            "data-done-button": "true",
            "data-live-search": "true",
            "data-live-search-placeholder": "Search",
            "data-actions-box": "true",
        },
        coerce=str,
        # choices=[(0, '公用'), (1, '私人')]
    )
    user_remarks = TextAreaField(
        validators=[Length(max=255)],
        render_kw={
            'id': 'userremarks',
            'class': 'form-control',
            'rows': '3'
        }
    )

    def __init__(self, *args, **kwargs):  # 初始化下拉框选项
        super(SysUserForm, self).__init__(*args, **kwargs)
        self.role_type.choices = [(role.id, role.name) for role in SysRole.query.all()]
        self.park_relation.choices = [(park.id, park.name) for park in ParkInfo.query.filter(ParkInfo.state == 1)]


    def get_errors(self):
        errors = ''
        for v in self.errors.values():
            for m in v:
                errors += m
            errors += '\n'
        return errors


class ParkDataForm(FlaskForm):
    """
    停车场信息页面表单
    """
    inputName = StringField(  # '停车场名称',
        validators=[DataRequired("请输入停车场名称"), Length(min=2, max=20)],
        render_kw={
            'id': 'inputName',
            'class': 'form-control',
            'required': 'required',
        }
    )
    inputContact = StringField(  # '联系人',
        render_kw={
            'id': 'inputContact',
            'class': 'form-control',
        }
    )
    inputMobile = StringField(  # '联系电话',
        # validators=[Regexp("1[35789]\d{9}", message="手机格式不正确")],
        render_kw={
            'id': 'inputMobile',
            'class': 'form-control',
        }
    )
    inputAddress = StringField(   # '地址',
        validators=[DataRequired('请输入停车场地址'), Length(3, 50)],
        render_kw={
            'id': 'inputAddress',
            'class': 'form-control',
            'required': 'required',
        }
    )
    inputLongitude = DecimalField(  # '经度'
        validators=[DataRequired('请正确填写经度')],
        render_kw={
            'id': 'inputLongitude',
            'class': 'form-control'
        }
    )
    inputLatitude = DecimalField(  # '纬度'
        validators=[DataRequired('请正确填写纬度')],
        render_kw={
            'id': 'inputLatitude',
            'class': 'form-control'
        }
    )
    inputType = SelectField(  # 停车场类型
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

# 用户添加页面
class AddUser(SysUserForm):

    newpwd = PasswordField(
            validators=[
                DataRequired("请输入密码！")
            ],
            render_kw={
                "id": "newpwd",
                "class": "form-control",
                "placeholder": "请设置登录密码",
                "required": "required"
            }
        )
    conpwd = PasswordField(
        validators=[
            DataRequired("请输入管理员重复密码！"),
            EqualTo('newpwd',message="密码不一致！")
        ],
        render_kw={
            "id": "conpwd",
            "class": "form-control",
            "placeholder": "请确认密码",
            "required": "required"
        }
    )

# 修改密码验证表单
# class PwdUpdate(FlaskForm):
#
#     newpwd = PasswordField(
#         validators=[
#             DataRequired("请输入密码！")
#         ],
#         render_kw={
#             "id": "newpwd",
#             "class": "form-control",
#             "placeholder": "请设置登录密码",
#             "required": "required"
#         }
#     )
#     repwd = PasswordField(
#         validators=[
#             DataRequired("请输入管理员重复密码！"),
#             EqualTo('newpwd',message="密码不一致！")
#         ],
#         render_kw={
#             "id": "conpwd",
#             "class": "form-control",
#             "placeholder": "请再次填写密码！",
#             "required": "required"
#         }
#     )