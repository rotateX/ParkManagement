from . import api
from ..models import CarInOut
from flask import request
from .. import db
from .decorators import permission_required
from ..models import Permissions


@api.route('/car_in_out/', methods=['POST'])
def new_car_in_out():
    car_in_out = CarInOut.from_json(request.json)  # 接收新的实例对象
    if car_in_out.in_time is None:                  # 进车信息添加
        car_in_out.stay_time = request.json.get('in_time')  # 添加其他属性，如，应收金额、订单号等
        pass
    else:                                                    # 出车信息添加
        car_in_out.stay_time = request.json.get('out_time')
        pass
        db.session.add(car_in_out)
        db.session.commit()
    return 201
