#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask_cors import CORS

views_blueprint = Blueprint('views', __name__)

CORS(views_blueprint)

from . import fulllog
from . import fulllog_batch
from . import wirelist
from . import fixture
from . import newlog
from . import newlog_batch
from . import testjet_limit
from . import ICT_result

