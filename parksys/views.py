# -*- coding : utf-8 -*-

from flask import Blueprint
from flask import Flask, url_for, render_template, redirect, request, flash, jsonify
from parksys.models import *
from parksys.parkdataform import ParkDataForm
import json
import uuid


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
    if request.method == 'POST':
        parkdata = json.loads(request.get_data())
        # print(parkdata)
        # print(type(parkdata))
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
            park_list = {
                # "id": park.id,
                "name": park.name,
                "addr": park.address,
                "contact": park.contact,
                "type": park.type,
                "state": park.state,
                "DT_RowId": park.id,
            }
            data.append(park_list)
        res = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': data,
        }
        print(jsonify(res))
        return jsonify(res)
    else:
        return render_template('parksys/parkinfo.html')


# 停车场创建页面
@parksys.route('/newpark', methods=['GET', 'POST'])
def newpark():
    dataform = ParkDataForm()
    res = {}
    if request.method == 'POST':
        if dataform.validate_on_submit():
            # print(type(dataform.data))
            # print(dataform.data)
            name = dataform.inputName.data.strip()
            contact = dataform.inputContact.data.strip()
            mobile = dataform.inputMobile.data.strip()
            address = dataform.inputAddress.data.strip()
            longitude = dataform.inputLongitude.data
            latitude = dataform.inputLatitude.data
            parktype = dataform.inputType.data
            monthlyparking = dataform.inputMonthlyParking.data
            chargingrules = dataform.inputChargingRules.data
            remarks = dataform.inputParkRemarks.data
            park = ParkInfo(
                id=str(uuid.uuid4()),
                name=name,
                contact=contact,
                mobile=mobile,
                address=address,
                longitude=longitude,
                latitude=latitude,
                create_by='admin',
                type=int(parktype),
                monthly_parking_space=monthlyparking,
                charging_rules=chargingrules,
                remarks=remarks,
            )
            try:
                db.session.add(park)
                db.session.commit()
                print('添加成功')
                res['status'] = 'success'
            except Exception as err:
                res['status'] = 'error'
                print('写入数据库失败')
                print(err)
        else:
            res['status'] = 'failed'
            res['message'] = dataform.get_errors()
            print(res['message'])
        return jsonify(res)
    else:
        return render_template('parksys/newpark.html', dataform=dataform)


# 删除停车场
@parksys.route('/delpark', methods=['POST'])
def delpark():
    res = {}
    parkid = request.get_data()
    # print(parkid)
    park = ParkInfo.query.get(parkid)
    if park:
        try:
            park.state = 0
            db.session.commit()
            res['status'] = 'success'
        except Exception as err:
            res['status'] = 'error'
            print('数据库出错：' + str(err))
    else:
        res['status'] = 'failed'
    return res


# 点击修改停车场信息
@parksys.route('/updatepark/', methods=['GET'])
def updatepark():
    dataform = ParkDataForm()
    if request.method == 'GET':
        park_id = request.args.get('parkcode')
        print('updatepark: ' + park_id)
        park = ParkInfo.query.get(park_id)
        if park:
            return render_template('parksys/updatepark.html', park=park, dataform=dataform)
        else:
            return redirect(url_for('parksys.getpark'))


#  修改停车场信息
@parksys.route('/updating/<parkcode>', methods=['POST'])
def updating(parkcode):
    dataform = ParkDataForm()
    res = {}
    # print('打印parkcode: ' + parkcode)
    # print('打印接收的dataform: ')
    print(dataform.data)
    if dataform.validate_on_submit():
        park = ParkInfo.query.get(parkcode)
        # print('打印park信息: ')
        # print(park)
        park.name = dataform.inputName.data.strip()
        park.contact = dataform.inputContact.data.strip()
        park.mobile = dataform.inputMobile.data.strip()
        park.address = dataform.inputAddress.data.strip()
        park.longitude = dataform.inputLongitude.data
        park.latitude = dataform.inputLatitude.data
        park.type = dataform.inputType.data
        park.monthly_parking_space = dataform.inputMonthlyParking.data
        park.charging_rules = dataform.inputChargingRules.data
        park.remarks = dataform.inputParkRemarks.data
        try:
            db.session.commit()
            print('保存成功')
            res['status'] = 'success'
        except Exception as err:
            res['status'] = 'error'
            print('写入数据库失败')
            print(err)
    else:
        res['status'] = 'failed'
        res['message'] = dataform.get_errors()
        print(res['message'])
    return jsonify(res)
