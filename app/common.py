#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint,current_app, request, make_response, jsonify
from flask_restful import Resource, Api

# from . import views_blueprint
from app.extensions import mysql2,restapi,cache
from app.utils import cache_key
from flask import request
import textwrap
import gzip
import logging
import json
import decimal
import os
from datetime import date,datetime as dt, timedelta
import base64
import random
import time


class Common(Resource):

    def BeforeNWeekDate(weeknum):
       # 取得今日星期幾
        wday=int(time.strftime("%w",time.localtime()))

        # 取得上週日日期後再往前推週數*7天就是n週前的星期日
        beforendays=weeknum*7
        after_enddate=(dt.now()-timedelta(days=wday))-timedelta(days=beforendays)
        return(after_enddate)

    def WeekNumList(weeknum):
        weeknumlist = []
        n_day = dt.now()
        x=1

        # 取得本日週數
        weeknumlist.append(n_day.isocalendar()[1])

        # 往前推算n次7天
        for x in range(weeknum-1):
            # 若weeknum是正數，則代表需要往後推算n週
            # if(weeknum>0):
            #     n_day = n_day + timedelta(days=7)
            # # 若weeknum是負數，則代表需要往前推算n週
            # else:
                # n_day = n_day - timedelta(days=7)
            n_day = n_day - timedelta(days=7)

            weeknumlist.append(n_day.isocalendar()[1])

            x=x+1

        return (weeknumlist)

    def FetchDB(query):
        try:
            conn = mysql2.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            result=cursor.fetchall()
            return (result)
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()











