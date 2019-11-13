# -*- coding : utf-8 -*-

from flask import Blueprint
from flask import Flask, url_for, render_template, redirect, request, flash, jsonify
from parksys.models import *
from parksys.parkdataform import ParkDataForm, LoginForm
import json
import uuid
from logger import Logger
import datetime
import re

logger = Logger(logger='parksys').getlog()

parksys = Blueprint(
    'parksys',
    __name__,
    url_prefix='/parksys',
    template_folder='templates/parksys',
    static_folder='static'
)

# 登录页面
@parksys.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    return render_template('parksys/login.html', loginform=loginform)

# 退出


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
        searchstr = ''.join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', parkdata['search'])) # 过滤特殊字符
        recordsTotal = ParkInfo.query.filter(ParkInfo.state == 1).count()  # 未过滤记录数
        if searchstr:
            recordsFiltered = ParkInfo.query.filter(ParkInfo.state==1, ParkInfo.name.like("%" + searchstr + "%")).count() # 过滤后的记录
            pagination = ParkInfo.query.filter(ParkInfo.state==1, ParkInfo.name.like("%" + searchstr + "%")).order_by(ParkInfo.create_on.desc()).paginate(
                page=page, per_page=length, error_out=True)
        else:
            recordsFiltered = ParkInfo.query.filter(ParkInfo.state==1).count() # 过滤后的记录
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
                # print('添加成功')
                logger.info('newpark - <%s> 停车场创建成功' % name)
                res['status'] = 'success'
            except Exception as err:
                res['status'] = 'error'
                logger.info('newpark - <%s> 停车场写入数据库失败，错误： %s' % (name, str(err)))
                # print('写入数据库失败')
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
            logger.info('delpark - 删除 <%s> 停车场成功' % park.name)
        except Exception as err:
            res['status'] = 'error'
            logger.info('delpark - 删除 <%s> 停车场时出错，错误： %s' % (park.name, str(err)))
            # print('数据库出错：' + str(err))
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
            # print('保存成功')
            logger.info('updating - <%s> 停车场信息修改成功' % park.name)
            res['status'] = 'success'
        except Exception as err:
            res['status'] = 'error'
            # print('写入数据库失败')
            logger.info('updating - <%s> 停车场信息修改失败，错误： %s' % (park.name, str(err)))
            # print(err)
    else:
        res['status'] = 'failed'
        res['message'] = dataform.get_errors()
        print(res['message'])
    return jsonify(res)


# 过车信息页面
@parksys.route('/carinout', methods=['GET', 'POST'])
def carinout():
    if request.method == 'POST':
        parkdata = json.loads(request.get_data())
        draw = parkdata['draw']
        start = parkdata['start']
        length = parkdata['length']
        # page = start // length + 1  # 计算页码
        page = parkdata['page']
        carno = ''.join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', parkdata['carno']))  # 只提取中文、英文、数字
        parkname = ''.join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', parkdata['parkname']))
        try:
            begintime = datetime.datetime.strptime(parkdata['begintime'], "%Y-%m-%d %H:%M:%S")
            endtime = datetime.datetime.strptime(parkdata['endtime'], "%Y-%m-%d %H:%M:%S")
        except Exception as errstrtime:
            # 获取不到时间时默认请求当天数据
            now = datetime.datetime.now()
            begintime = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                                 microseconds=now.microsecond)
            endtime = begintime + datetime.timedelta(hours=23, minutes=59, seconds=59)
            print(str(errstrtime))

        # 未过滤记录数
        recordsTotal = CarInOut.query.filter(
            CarInOut.in_time <= endtime,
            CarInOut.in_time >= begintime
        ).count()
        if parkname:
            park_list = []
            parkobj = ParkInfo.query.filter(ParkInfo.name.like("%" + parkname + "%")) # 停车场对象
            for park in  parkobj:
                park_list.append(park.id)
            recordsFiltered = CarInOut.query.filter(
                CarInOut.in_time <= endtime,
                CarInOut.in_time >= begintime,
                CarInOut.plate_no.like("%" + carno + "%") if carno is not None else "",
                CarInOut.park_id.in_(park_list),
            ).count()  # 过滤后的记录

            pagination = CarInOut.query.filter(
                CarInOut.in_time <= endtime,
                CarInOut.in_time >= begintime,
                CarInOut.plate_no.like("%" + carno + "%") if carno is not None else "",
                CarInOut.park_id.in_(park_list),
            ).order_by(
                CarInOut.in_time.desc()).paginate(
                page=page, per_page=length, error_out=True)
        else:
            recordsFiltered = CarInOut.query.filter(
                CarInOut.in_time <= endtime,
                CarInOut.in_time >= begintime,
                CarInOut.plate_no.like("%" + carno + "%") if carno is not None else "",
            ).count()  # 过滤后的记录
            pagination = CarInOut.query.filter(
                CarInOut.in_time <= endtime,
                CarInOut.in_time >= begintime,
                CarInOut.plate_no.like("%" + carno + "%") if carno is not None else "",
            ).order_by(
                CarInOut.in_time.desc()).paginate(
                page=page, per_page=length, error_out=True)
        cars = pagination.items
        data = []
        for car in cars:
            # print(car.in_time.strftime("%Y-%m-%d %H:%M:%S"))
            if car.out_time:
                out_time = car.out_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                out_time = ''
            park_list = {
                # "id": park.id,
                "id": car.id,
                "parkname": car.parkinfo.name,
                "plate_no": car.plate_no,
                "in_time": car.in_time.strftime("%Y-%m-%d %H:%M:%S"),
                "out_time": out_time,
                "in_port": car.in_port,
                "out_port": car.out_port,
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
        return render_template('parksys/carinout.html')

