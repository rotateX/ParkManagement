# -*- coding : utf-8 -*-

from flask import Blueprint
from flask import Flask, url_for, render_template, redirect, request, flash
from parksys.models import *
from parksys.parkdataform import ParkDataForm

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
    parks = ParkInfo.query.all()
    for park in parks:
        list = [park.id, park.name, park.address, park.contact, park.type, park.state]
        dataSet.append(list)
    return render_template('parksys/parkinfo.html', dataSet=dataSet)

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
