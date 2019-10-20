# -*- coding : utf-8 -*-

from flask import Blueprint
from flask import Flask, url_for, render_template, redirect, request, flash, jsonify
from parksys.models import *
from parksys.parkdataform import ParkDataForm
import json


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
@parksys.route('/parkinfo', methods=['GET'])
def getpark():
    dataSet = []
    parks = ParkInfo.query.order_by(ParkInfo.create_on.desc()).all()
    for park in parks:
        list = [park.id, park.name, park.address, park.contact, park.type, park.state]
        dataSet.append(list)
    return render_template('parksys/parkinfo.html', dataSet=dataSet)


# 停车场信息页面测试
@parksys.route('/parkinfotest', methods=['GET','POST'])
def getparktest():

    if request.method == 'POST':
        # draw = request.data['draw']

        parkdata = json.loads(request.get_data())
        print(parkdata)
        print(type(parkdata))
        draw = parkdata['draw']
        start = parkdata['start']
        length = parkdata['length']
        # page = start // length + 1  # 计算页码
        page = parkdata['page']
        # recordsTotal = ParkInfo.query.order_by(ParkInfo.create_on.desc()).count()  # 未过滤记录数
        recordsFiltered = ParkInfo.query.filter(ParkInfo.state==1).order_by(ParkInfo.create_on.desc()).count() # 过滤后的记录
        recordsTotal = recordsFiltered
        pagination = ParkInfo.query.filter(ParkInfo.state==1).order_by(ParkInfo.create_on.desc()).paginate(
            page=page, per_page=length, error_out=True)
        parks = pagination.items
        data = []
        for park in parks:
            list = [park.id, park.name, park.address, park.contact, park.type, park.state]
            data.append(list)
        res = {
            'draw': 1,
            'recordsTotal' :recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': data,
        }
        print(jsonify(res))
        return jsonify(res)
    else:
        return render_template('parksys/test.html')

# 停车场创建页面
@parksys.route('/newpark', methods=['GET', 'POST'])
def newpark():
    dataform = ParkDataForm()
    res = {}
    if request.method == 'POST':
        if dataform.validate_on_submit():
            res['status'] = 'success'
            name = dataform.inputName.data
            request.get_data('id')
            address = dataform.inputAddress.data
            print(name, address)
            flash('创建成功')
            return redirect(url_for('getpark'))
        else:
            res['status'] = 'failed'
            flash('创建失败')
    else:
        return render_template('parksys/newpark.html', dataform=dataform)


# # 停车场信息保存
# @parksys.route('/savepark', methods=['POST'])
# def savepark():
#     res = {}
#     if request.method == 'POST':
#         name = request.form.get('inputName')
#         print('od' + str(name))
#         res['status'] = 'success'
#         return res

# 删除停车场
@parksys.route('/delpark', methods=['POST'])
def delpark():
    res = {}
    parkid = request.get_data()
    park = ParkInfo.query.get(parkid)
    if park:
        park.state = 0
        db.session.commit()
        res['status'] = 'success'
    else:
        res['status'] = 'failed'
    return res

# 修改停车场信息
@parksys.route('/updatepark', methods=['GET', 'POST'])
def updatepark(park_id):
    park = ParkInfo.query.get(park_id)
    if park:
        return render_template('parksys/updatepark.html', park=park)
    else:
        pass
