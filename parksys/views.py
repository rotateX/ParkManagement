# -*- coding : utf-8 -*-

from flask import Blueprint
from flask import Flask, url_for, render_template, redirect, request
from parksys.models import *

parksys = Blueprint(
    'parksys',
    __name__,
    url_prefix='/parksys',
    template_folder='templates/parksys',
    static_folder='static'
)

# 平台首页
@parksys.route('/index', methods=['GET'])
def indexpage():
    return render_template('parksys/index.html')


# 停车场信息页面
@parksys.route('/parkinfo', methods=['GET', 'POST'])
def getpark():
    dataSet = []
    parks = ParkInfo.query.all()
    for park in parks:
        list = [park.name, park.address, park.contact, park.type, park.state]
        dataSet.append(list)
    return render_template('parksys/parkinfo.html', dataSet=dataSet)

# 停车场创建页面
@parksys.route('/newpark', methods=['GET'])
def newpark():
    return render_template('parksys/newpark.html')