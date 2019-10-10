# -*- coding : utf-8 -*-

from flask import Blueprint

parkapi = Blueprint(
    'parkapi',
    __name__,
    url_prefix='/parkapi',
    template_folder='templates/parkapi',
    static_folder='static'
)

