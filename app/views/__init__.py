#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint

views_blueprint = Blueprint('views', __name__)

from . import demoapi
from . import wirelist
from . import fixture
from . import demoapi_batch
from . import newlog_batch
from . import newlog
