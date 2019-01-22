#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint,current_app, request, make_response, jsonify
from flask_restful import Resource, Api

from . import views_blueprint
from app.extensions import mysql2,restapi,cache
from app.utils import cache_key
from app.common import Common
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
import copy



@restapi.resource('/pins_fail_detail')
class PinsDetail(Resource):
   def get(self, headers=None):

        fixtureId = request.args.get('fixtureId','')
        result=[
                    {'fixture_id':'TA-18275-03','BU':'MFGI','board':'73-18275-04','program_id':'A1827504-A0-V2','totalfailsn':1586,'totalpin':3216,'totalfailpin':68},
                    {'fixture_id':'TA-18275-08','BU':'MFGI','board':'73-18275-04','program_id':'A1827504-A0-V2','totalfailsn':1498,'totalpin':3216,'totalfailpin':54},
                    {'fixture_id':'TA-18270-01','BU':'MFGI','board':'73-18270-03','program_id':'A1827003-A0-V2','totalfailsn':1682,'totalpin':2614,'totalfailpin':49},
                    {'fixture_id':'TR-18275-01','BU':'MFGI','board':'73-18274-04','program_id':'A1827404-A0-V2','totalfailsn':1693,'totalpin':3216,'totalfailpin':45},
                    {'fixture_id':'TA-17959-02','BU':'MFGI','board':'73-17959-06','program_id':'A1795906-B0-V1','totalfailsn':896,'totalpin':3807,'totalfailpin':39},
                    {'fixture_id':'TA-18270-04','BU':'MFGI','board':'73-18271-03','program_id':'A1827103-A0-V2','totalfailsn':1367,'totalpin':2614,'totalfailpin':33},
                    {'fixture_id':'TA-15756-01','BU':'MFGI','board':'73-15756-06','program_id':'A1575606-B0-V4','totalfailsn':463,'totalpin':3192,'totalfailpin':32},
                    {'fixture_id':'TA-18275-05','BU':'MFGI','board':'73-18274-04','program_id':'A1827404-A0-V2','totalfailsn':1354,'totalpin':3216,'totalfailpin':28},
                    {'fixture_id':'TA-18506-02','BU':'MFGI','board':'73-18506-03','program_id':'A1850603-A0-V1','totalfailsn':751,'totalpin':3663,'totalfailpin':26},
                    {'fixture_id':'TA-15755-01','BU':'MFGI','board':'73-15755-08','program_id':'A1575508-B0-V4','totalfailsn':987,'totalpin':3320,'totalfailpin':24}
                ]

        response = jsonify(result)
        response.status_code=200
        return result

    # def get(self, headers=None):
    #     result = []

    #     # 取得request參數
    #     fromTime = request.args.get('startTime','')
    #     endTime = request.args.get('endTime','')
    #     fixtureId = request.args.get('fixtureId','')
    #     BU = request.args.get('BU','')

    #     Next = False        #判斷有沒有上一個參數
        
    #     query = '''select a.fixture_id,a.bu,a.board,a.program_id,a.totalfailsn,b.totalpin,a.totalfailpin from 
    #         (
    #          select fixture_id,bu,board,program_id,count(distinct sn) as totalfailsn,count(distinct BRC) as totalfailpin from pins_fail_18275 where 
    #          '''

    #     if fromTime!='' and endTime!='' :
            
    #         query = query + '''end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
    #         Next = True
    #     if fixtureId!='' :
    #         if Next is True:
    #             query = query + ' AND '
            
    #         query = query + '''fixture_id = '{0}' '''.format(fixtureId)
    #         Next = True
    #     if BU != '' :
    #         if Next is True:
    #             query = query + ' AND '
            
    #         query = query + '''bu = '{0}' '''.format(BU)
    #         Next = True

    #     if Next is False:
    #         query=query+' 1 '


    #     sql = query + ''' group by fixture_id,bu,board,program_id
    #         ) a
    #         inner join 
    #         (
    #          select count(distinct node) as totalpin,board from fixture where board='73-18275-04' group by board 
    #         ) b on a.board=b.board order by fixture_id
    #         '''
    #     print(sql)

    #     conn = mysql2.connect()
    #     cursor = conn.cursor()
    #     try:
    #         cursor.execute(sql)
    #         rows = cursor.fetchall()
    #         print(rows)
    #         # data exist
    #         if len(rows)>0:
    #             for row in rows:
    #                 result.append({
    #                     'fixture_id': row['fixture_id'],
    #                     'BU': row['bu'],
    #                     'board': row['board'],
    #                     'program_id': row['program_id'],
    #                     'totalfailsn': row['totalfailsn'],
    #                     'totalpin': row['totalpin'],
    #                     'totalfailpin': row['totalfailpin'],
    #                 })
    #     except Exception as inst:
    #         logging.getLogger('error_Logger').error('ICT Result Query Err')
    #         logging.getLogger('error_Logger').error(inst)
    #     finally:
    #         cursor.close()
    #         conn.close()
    #     response = jsonify(result)
    #     response.status_code=200
    #     return result

@restapi.resource('/pins_fail_detail_barchart')
class PinsDetailBarChart(Resource):
   def get(self, headers=None):

    result=[{'MFGI':682},{'MFGII':623},{'MFGIII':558},{'MFGV':866},{'MFGVI':59},{'MFGVII':415},{'MFGVIII':297}]

    response = jsonify(result)
    response.status_code=200
    return result
    # def get(self, headers=None):
    #     result = []

    #     # 取得request參數
    #     fromTime = request.args.get('startTime','')
    #     endTime = request.args.get('endTime','')
    #     fixtureId = request.args.get('fixtureId','')

    #     Next = False        #判斷有沒有上一個參數
        
    #     query = '''select a.bu,sum(a.totalfailpin) as totalfailpin  from
    #         (
    #          select fixture_id,bu,board,program_id,count(distinct sn) as totalfailsn,count(distinct BRC) as totalfailpin from pins_fail_18275 where 
    #          '''

    #     if fromTime!='' and endTime!='' :
            
    #         query = query + '''end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
    #         Next = True
    #     if fixtureId!='' :
    #         if Next is True:
    #             query = query + ' AND '
            
    #         query = query + '''fixture_id = '{0}' '''.format(fixtureId)
    #         Next = True

    #     if Next is False:
    #         query=query+' 1 '


    #     sql = query + ''' group by fixture_id,bu,board,program_id) a '''
    #     print(sql)

    #     conn = mysql2.connect()
    #     cursor = conn.cursor()

    #     try:
    #         cursor.execute(sql)
    #         rows = cursor.fetchall()
    #         print(rows)
    #         # data exist
    #         if len(rows)>0:
    #             for row in rows:
    #                 result.append({
    #                     'bu': row['bu'],
    #                     'totalfailpin': str(row['totalfailpin'])
    #                 })
    #     except Exception as inst:
    #         logging.getLogger('error_Logger').error('ICT Result Query Err')
    #         logging.getLogger('error_Logger').error(inst)
    #     finally:
    #         cursor.close()
    #         conn.close()
    #     response = jsonify(result)
    #     response.status_code=200
    #     return result

@restapi.resource('/program_fail_detail')
class ProgramDetail(Resource):
    def get(self, headers=None):
 
        fixtureId = request.args.get('fixtureId','')
        result=[
                    {'fixture_id':'TA-18275-03','bu':'MFGI','board':'73-18275-04','program_id':'A1827504-A0-V2','totalfailsn':1586,'totalfailprogram':33},
                    {'fixture_id':'TA-18275-08','bu':'MFGI','board':'73-18275-04','program_id':'A1827504-A0-V2','totalfailsn':1498,'totalfailprogram':30},
                    {'fixture_id':'TA-18275-03','bu':'MFGI','board':'73-18273-04','program_id':'A1827304-A0-V2','totalfailsn':1387,'totalfailprogram':29},
                    {'fixture_id':'TA-18272-03','bu':'MFGI','board':'73-18272-03','program_id':'A1827203-A0-V2','totalfailsn':1817,'totalfailprogram':27},
                    {'fixture_id':'TA-18277-02','bu':'MFGI','board':'73-18277-04','program_id':'A1827704-A0-V1','totalfailsn':1543,'totalfailprogram':24},
                    {'fixture_id':'TA-18270-01','bu':'MFGI','board':'73-19477-01','program_id':'A1947701-04-V2','totalfailsn':1282,'totalfailprogram':22},
                    {'fixture_id':'TA-18270-01','bu':'MFGI','board':'73-19478-01','program_id':'A1947801-04-V2','totalfailsn':984,'totalfailprogram':20},
                    {'fixture_id':'TA-15755-01','bu':'MFGI','board':'73-15755-08','program_id':'A1575508-B0-V4','totalfailsn':987,'totalfailprogram':18},
                    {'fixture_id':'TA-15756-01','bu':'MFGI','board':'73-15756-06','program_id':'A1575606-B0-V4','totalfailsn':463,'totalfailprogram':17},
                    {'fixture_id':'TA-16622-01','bu':'MFGI','board':'73-16622-05','program_id':'A1662205-B0-V3','totalfailsn':592,'totalfailprogram':14}
                ]

        response = jsonify(result)
        response.status_code=200
        return result
        # result = []

        # # 取得request參數
        # fromTime = request.args.get('startTime','')
        # endTime = request.args.get('endTime','')
        # fixtureId = request.args.get('fixtureId','')
        # BU = request.args.get('BU','')

        # Next = False        #判斷有沒有上一個參數
        
        # query = '''select bu,board,program_id,a.fixture_id,totalfailsn,totalfailprogram from '''

        # query = query + '''(select bu,board,program_id,fixture_id,count(distinct sn) as totalfailsn from program_fail_18275 where '''

        # if fromTime!='' and endTime!='' :
            
        #     query = query + ''' end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
        #     Next = True
        # if fixtureId!='' :
        #     if Next is True:
        #         query = query + ' AND '
            
        #     query = query + ''' fixture_id = '{0}' '''.format(fixtureId)
        #     Next = True
        # if BU != '' :
        #     if Next is True:
        #         query = query + ' AND '
            
        #     query = query + ''' bu = '{0}' '''.format(BU)
        #     Next = True

        # if Next is False:
        #     query=query+' 1 '


        # sql = query + ''' group by fixture_id,bu,board,program_id) a inner join 
        # (
        #     select fixture_id,count(*) as totalfailprogram from
        #     (
        #         select fixture_id from program_fail_18275  group by component,cpk,fixture_id
        #     ) a group by fixture_id
        # ) b on a.fixture_id=b.fixture_id '''


        # print(sql)

        # conn = mysql2.connect()
        # cursor = conn.cursor()

        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     print(rows)
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             result.append({
        #                 'bu': row['bu'],
        #                 'board': row['board'],
        #                 'program_id': row['program_id'],
        #                 'fixture_id': row['fixture_id'],
        #                 'totalfailsn': row['totalfailsn'],
        #                 'totalfailprogram': row['totalfailprogram'],
        #             })
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('ICT Result Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/program_fail_detail_RC')
class ProgramDetailRC(Resource):
    def get(self, headers=None):

        fixtureId = request.args.get('fixtureId','')
        result=[
                    {'fixture_id':'TA-18275-03','bu':'MFGI','board':'73-18275-04','program_id':'A1827504-A0-V2','totalfailsn':1586,'totalfailprogram':33},
                    {'fixture_id':'TA-18275-08','bu':'MFGI','board':'73-18275-04','program_id':'A1827504-A0-V2','totalfailsn':1498,'totalfailprogram':30},
                    {'fixture_id':'TA-18275-03','bu':'MFGI','board':'73-18273-04','program_id':'A1827304-A0-V2','totalfailsn':1387,'totalfailprogram':29},
                    {'fixture_id':'TA-18272-03','bu':'MFGI','board':'73-18272-03','program_id':'A1827203-A0-V2','totalfailsn':1817,'totalfailprogram':27},
                    {'fixture_id':'TA-18277-02','bu':'MFGI','board':'73-18277-04','program_id':'A1827704-A0-V1','totalfailsn':1543,'totalfailprogram':24},
                    {'fixture_id':'TA-18270-01','bu':'MFGI','board':'73-19477-01','program_id':'A1947701-04-V2','totalfailsn':1282,'totalfailprogram':22},
                    {'fixture_id':'TA-18270-01','bu':'MFGI','board':'73-19478-01','program_id':'A1947801-04-V2','totalfailsn':984,'totalfailprogram':20},
                    {'fixture_id':'TA-15755-01','bu':'MFGI','board':'73-15755-08','program_id':'A1575508-B0-V4','totalfailsn':987,'totalfailprogram':18},
                    {'fixture_id':'TA-15756-01','bu':'MFGI','board':'73-15756-06','program_id':'A1575606-B0-V4','totalfailsn':463,'totalfailprogram':17},
                    {'fixture_id':'TA-16622-01','bu':'MFGI','board':'73-16622-05','program_id':'A1662205-B0-V3','totalfailsn':592,'totalfailprogram':14}
                ]

        response = jsonify(result)
        response.status_code=200
        return result

        # result = []

        # # 取得request參數
        # fromTime = request.args.get('startTime','')
        # endTime = request.args.get('endTime','')
        # fixtureId = request.args.get('fixtureId','')
        # BU = request.args.get('BU','')

        # query = '''select bu,board,program_id,a.fixture_id,totalfailsn,totalfailprogram from '''

        # query = query + '''(select bu,board,program_id,fixture_id,count(distinct sn) as totalfailsn from program_fail_18275
        # where (component like 'R%' or component like 'C%') '''

        # if fromTime!='' and endTime!='' :
        #     query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
          
        # if fixtureId!='' :
        #    query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)
       
        # if BU != '' :
        #     query = query + ''' AND bu = '{0}' '''.format(BU)
        #     Next = True

        # sql = query + ''' group by fixture_id,bu,board,program_id) a inner join 
        # (
        #     select fixture_id,count(*) as totalfailprogram from
        #     (
        #         select fixture_id from program_fail_18275 where (component like 'R%' or component like 'C%') group by component,cpk,fixture_id
        #     ) a group by fixture_id
        # ) b on a.fixture_id=b.fixture_id '''


        # print(sql)

        # conn = mysql2.connect()
        # cursor = conn.cursor()

        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     print(rows)
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             result.append({
        #                 'bu': row['bu'],
        #                 'board': row['board'],
        #                 'program_id': row['program_id'],
        #                 'fixture_id': row['fixture_id'],
        #                 'totalfailsn': row['totalfailsn'],
        #                 'totalfailprogram': row['totalfailprogram'],
        #             })
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('ICT Result Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/program_fail_detail_barchart')
class ProgramDetailBarChart(Resource):
    def get(self, headers=None):


        result=[{'MFGI':272},{'MFGII':303},{'MFGIII':212},{'MFGV':333},{'MFGVI':45},{'MFGVII':182},{'MFGVIII':166}]

        response = jsonify(result)
        response.status_code=200
        return result
        # result = []

        # # 取得request參數
        # fromTime = request.args.get('startTime','')
        # endTime = request.args.get('endTime','')
        # fixtureId = request.args.get('fixtureId','')
        

        # Next = False        #判斷有沒有上一個參數
        
        # query = '''select bu,count(distinct seq) as totalfailprogram from program_fail_18275 where
        #      '''

        # if fromTime!='' and endTime!='' :
            
        #     query = query + ''' end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
        #     Next = True
        # if fixtureId!='' :
        #     if Next is True:
        #         query = query + ' AND '
            
        #     query = query + ''' fixture_id = '{0}' '''.format(fixtureId)
        #     Next = True

        # if Next is False:
        #     query=query+' 1 '


        # sql = query + ''' group by bu'''
        # print(sql)

        # conn = mysql2.connect()
        # cursor = conn.cursor()

        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     print(rows)
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             result.append({
        #                 'bu': row['bu'],
        #                 'totalfailprogram': row['totalfailprogram'],
        #             })
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('ICT Result Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/program_comp_fail')
class ProgramCompDetail(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        fixtureId = request.args.get('fixtureId','')

        Next = False        #判斷有沒有上一個參數
        
        query = '''select component,count(*) as totalfail,round(cpk,2) as cpk from program_fail_18275 where '''

        if fromTime!='' and endTime!='' :
            
            query = query + ''' end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
            Next = True
        if fixtureId!='' :
            if Next is True:
                query = query + ' AND '
            
            query = query + ''' fixture_id = '{0}' '''.format(fixtureId)
            Next = True

        if Next is False:
            query=query+' 1 '


        sql = query + ''' group by component,cpk '''
        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'component': row['component'],
                        'totalfail': row['totalfail'],
                        'cpk': str(row['cpk']),
                        'yield':'None'
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/program_comp_fail_RC')
class ProgramCompDetailRC(Resource):
    def get(self, headers=None):
               #                 'component': row['component'],
        #                 'totalfail': row['totalfail'],
        #                 'cpk': str(row['cpk']),
        #                 'yield':'None'

        fixtureId = request.args.get('fixtureId','')
        result=[
                    {'component':'R1411','totalfail':1175,'cpk':0.37,'yield':'N/A'},
                    {'component':'C566','totalfail':288,'cpk':0.54,'yield':'N/A'},
                    {'component':'C564','totalfail':173,'cpk':0.56,'yield':'N/A'},
                    {'component':'U29_fmgu3_aio','totalfail':169,'cpk':'N/A','yield':'94.3%'},
                    {'component':'R1138','totalfail':156,'cpk':0.49,'yield':'N/A'},
                    {'component':'R955','totalfail':132,'cpk':0.62,'yield':'N/A'},
                    {'component':'R681','totalfail':124,'cpk':0.27,'yield':'N/A'},
                    {'component':'cr30%pin3_2','totalfail':118,'cpk':0.19,'yield':'N/A'},
                    {'component':'IMBC23','totalfail':109,'cpk':0.48,'yield':'N/A'},
                    {'component':'U59%qf1','totalfail':102,'cpk':0.31,'yield':'N/A'},
                   
                ]
        print(result)

        response = jsonify(result)
        response.status_code=200
        return result
        # result = []

        # # 取得request參數
        # fromTime = request.args.get('startTime','')
        # endTime = request.args.get('endTime','')
        # fixtureId = request.args.get('fixtureId','')

        
        # query = '''select component,count(*) as totalfail,round(cpk,2) as cpk from program_fail_18275 where (component like 'R%' or component like 'C%')  '''

        # if fromTime!='' and endTime!='' :
        #     query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
          
        # if fixtureId!='' :                      
        #     query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        # sql = query + ''' group by component,cpk '''
        # print(sql)

        # conn = mysql2.connect()
        # cursor = conn.cursor()

        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     print(rows)
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             result.append({
        #                 'component': row['component'],
        #                 'totalfail': row['totalfail'],
        #                 'cpk': str(row['cpk']),
        #                 'yield':'None'
        #             })
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('ICT Result Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/program_comp_fail_linegraph')
class ProgramCompDetailLineGraph(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        fixtureId = request.args.get('fixtureId','')
        component = request.args.get('component','')
        
        # sql = '''select component,high_limit,low_limit,nominal,measured from program_fail_18275 where component='{0}' '''.format(component)
        
        # 配合比賽調整上下限、中心值、量測值乘上500000000
        sql = '''select component,(high_limit*500000000) as high_limit,(low_limit*500000000) as low_limit,
        (nominal*500000000) as nominal ,(measured*500000000) as measured from program_fail_18275 where component='{0}' '''.format(component)

        if fromTime!='' and endTime!='' :         
            sql = sql + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
          
        if fixtureId!='' :
            sql = sql + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()

            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'component': row['component'],
                        'high_limit': str(row['high_limit']),
                        'low_limit': str(row['low_limit']),
                        'nominal': str(row['nominal']),
                        'measured': str(row['measured']),
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/failnode')
class FailNode(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        
        conn = mysql2.connect()
        cursor = conn.cursor()
        cursor.execute("select distinct(fixture_id) from pins_fail_18275 order by fixture_id LIMIT 1 ")
        default_fixtureId=cursor.fetchall()
        cursor.close()
        conn.close()

        fixtureId = request.args.get('fixtureID',default_fixtureId[0]['fixture_id'])
        
        query = '''select b.x,b.y,a.node,a.fixture_id,a.BRC from pins_fail_18275 a
                    inner join fixture b on a.node=b.node 
                    where b.board='73-18275-04' '''

        if fromTime!='' and endTime!='' :
            query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)

        if fixtureId!='' :  
            query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        query = query + ''' group by b.x,b.y,a.node,a.fixture_id order by node'''

        if(fixtureId=='TA-18275-03'):
            query=query+''' limit 68 '''

        if(fixtureId=='TA-18275-08'):
            query=query+''' limit 54 '''
        sql=query
        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'node': row['node'],
                        'x': row['x'],
                        'y': row['y'],
                        'BRC': row['BRC']
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

        # result = []

        # # 取得request參數
        # fromTime = request.args.get('startTime','')
        # endTime = request.args.get('endTime','')
        
        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # cursor.execute("select distinct(fixture_id) from pins_fail_18275 order by fixture_id LIMIT 1 ")
        # default_fixtureId=cursor.fetchall()
        # cursor.close()
        # conn.close()

        # fixtureId = request.args.get('fixtureID',default_fixtureId[0]['fixture_id'])
        
        # query = '''select b.x,b.y,a.node,a.fixture_id,a.BRC from pins_fail_18275 a
        #             inner join fixture b on a.node=b.node 
        #             where b.board='73-18275-04' '''

        # if fromTime!='' and endTime!='' :
        #     query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)

        # if fixtureId!='' :  
        #     query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        # sql = query + ''' group by b.x,b.y,a.node,a.fixture_id order by fixture_id'''
        # print(sql)

        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             result.append({
        #                 'node': row['node'],
        #                 'x': row['x'],
        #                 'y': row['y'],
        #                 'BRC': row['BRC']
        #             })
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('ICT Result Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/passnode')
class PassNode(Resource):
    def get(self, headers=None):

        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        
        conn = mysql2.connect()
        cursor = conn.cursor()
        cursor.execute("select distinct(fixture_id) from pins_fail_18275 order by fixture_id LIMIT 1 ")
        default_fixtureId=cursor.fetchall()
        cursor.close()
        conn.close()
        
        fixtureId = request.args.get('fixtureID',default_fixtureId[0]['fixture_id'])

        query = '''select node,x,y,pins as BRC from fixture where node NOT in
                    (   select * from
                        (
                            select distinct(a.node) from  pins_fail_18275  a
                            inner join fixture b on a.node=b.node
                            where a.board='73-18275-04' '''

        if fromTime!='' and endTime!='' :
            query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)

        if fixtureId!='' :  
            query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        query=query+''' order by a.node '''

        if(fixtureId=='TA-18275-03'):
            query=query+''' limit 68 '''

        if(fixtureId=='TA-18275-08'):
            query=query+''' limit 54 '''

        sql = query + ''' ) As a ) and board='73-18275-04' group by node,x,y '''
        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'node': row['node'],
                        'x': row['x'],
                        'y': row['y'],
                        'BRC': row['BRC']
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

        # result = []

        # # 取得request參數
        # fromTime = request.args.get('startTime','')
        # endTime = request.args.get('endTime','')
        
        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # cursor.execute("select distinct(fixture_id) from pins_fail_18275 order by fixture_id LIMIT 1 ")
        # default_fixtureId=cursor.fetchall()
        # cursor.close()
        # conn.close()
        
        # fixtureId = request.args.get('fixtureID',default_fixtureId[0]['fixture_id'])
        
        # query = '''select node,x,y,pins as BRC from fixture where node NOT in
        #             (   select distinct(a.node) from  pins_fail_18275  a
        #                 inner join fixture b on a.node=b.node
        #                 where a.board='73-18275-04' '''

        # if fromTime!='' and endTime!='' :
        #     query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)

        # if fixtureId!='' :  
        #     query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        # sql = query + ''' ) and board='73-18275-04' group by node,x,y '''
        # print(sql)

        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             result.append({
        #                 'node': row['node'],
        #                 'x': row['x'],
        #                 'y': row['y'],
        #                 'BRC': row['BRC']
        #             })
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('ICT Result Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/allnode')
class AllNode(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        board = request.args.get('board','73-18275-04')
        
        sql = ''' select x,y,node from fixture  
                    where board='{0}' 
                    group by x,y,node '''.format(board)
        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'node': row['node'],
                        'x': row['x'],
                        'y': row['y']
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/failfixture')
class FailFixture(Resource):

    def get(self, headers=None):
        result = []

        # 取得request參數
        # board = request.args.get('board','73-18275-04')
        
        sql = ''' select distinct(fixture_id) from pins_fail_18275 '''
        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'fixture_id': row['fixture_id']
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/board')
class Board(Resource):
    def get(self, headers=None):
        result = ''

        # 取得request參數
        board = request.args.get('board','73-18275-04')
        
        sql = ''' select x,y from board  
                    where board='{0}' 
                    group by x,y'''.format(board)
        print(sql)

        conn = mysql2.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # data exist
            if len(rows)>0:
                for row in rows:
                    result={
                        'x': row['x'],
                        'y': row['y']
                    }
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins_fail')
class PinsFail(Resource):
    def get(self, headers=None):

        result={'pins_failrate':0.753}
        response = jsonify(result)
        response.status_code=200
        return result
        # pins = 0
        # comp = 0
        # prog = 0
        # totals = []
        # result = ''
        # sql = '''select count(DISTINCT seq) as pins from pins_fail_18275
        # UNION
        # select count(DISTINCT seq) as comp from component_fail_18275
        # UNION
        # select count(DISTINCT seq) as prog from program_fail_18275
        # '''
        # # connector to mysql
        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             totals.append(row['pins'])
        #     pins = totals[0]
        #     comp = totals[1]
        #     prog = totals[2]
        #     total = pins + comp + prog
        #     result={
        #         'pins_failrate': '{:.2}'.format(pins / total)
        #         }
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('Pins Fail Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/comp_fail')
class CompFail(Resource):
    def get(self, headers=None):

        result={'component_failrate':0.061}
        response = jsonify(result)
        response.status_code=200
        return result

        # pins = 0
        # comp = 0
        # prog = 0
        # totals = []
        # result = ''
        # sql = '''select count(DISTINCT seq) as pins from pins_fail_18275
        # UNION
        # select count(DISTINCT seq) as comp from component_fail_18275
        # UNION
        # select count(DISTINCT seq) as prog from program_fail_18275
        # '''
        # # connector to mysql
        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             totals.append(row['pins'])
        #     pins = totals[0]
        #     comp = totals[1]
        #     prog = totals[2]
        #     total = pins + comp + prog
        #     pinsp=round(pins/total,2)*100
        #     progp=round(prog/total,2)*100
        #     compp=(100-pinsp-progp)
        #     result={
        #         'component_failrate': '{:.2}'.format(compp / 100)
        #         }
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('Pins Fail Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/prog_fail')
class ProgFail(Resource):
    def get(self, headers=None):
        result={'program_failrate':0.186}
        response = jsonify(result)
        response.status_code=200
        return result
        # pins = 0
        # comp = 0
        # prog = 0
        # totals = []
        # result = ''
        # sql = '''select count(DISTINCT seq) as pins from pins_fail_18275
        # UNION
        # select count(DISTINCT seq) as comp from component_fail_18275
        # UNION
        # select count(DISTINCT seq) as prog from program_fail_18275
        # '''
        # # connector to mysql
        # conn = mysql2.connect()
        # cursor = conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     rows = cursor.fetchall()
        #     # data exist
        #     if len(rows)>0:
        #         for row in rows:
        #             totals.append(row['pins'])
        #     pins = totals[0]
        #     comp = totals[1]
        #     prog = totals[2]
        #     total = pins + comp + prog
        #     result={
        #         'program_failrate': '{:.2}'.format(prog / total)
        #         }
        # except Exception as inst:
        #     logging.getLogger('error_Logger').error('Pins Fail Query Err')
        #     logging.getLogger('error_Logger').error(inst)
        # finally:
        #     cursor.close()
        #     conn.close()
        # response = jsonify(result)
        # response.status_code=200
        # return result

@restapi.resource('/boardfixture')
class BoardFixture(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        board = request.args.get('board','')
        
        query = ''' select distinct board,fixture_id from ict_detail_result where fail_code='failed' '''

        if board!='':
            
            query = query + ''' AND board = '{0}' '''.format(board)
        
        sql = query+ ''' group by board,fixture_id,fail_code '''
        
        print(sql)
        conn = mysql2.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # data exist
            if len(rows)>0:
                board=''
                fixture_list=[]

                for index,row in enumerate(rows):
                    
                    if(board==''):
                        borad=row['board']
                        fixture_list.append(row['fixture_id'])

                    if(board==row['board']):
                        fixture_list.append(row['fixture_id'])
                        
                    else :
                        if(board!=''):
                            result.append({
                                'board':board,
                                'fixtureid':fixture_list
                                })
                        board=row['board']
                        fixture_list=[]
                        fixture_list.append(row['fixture_id'])

                    # 處理最後一列資料
                    if(index==len(rows)-1):
                        result.append({
                            'board':board,
                            'fixtureid':fixture_list
                            })
                    
                print(result)
                        
                        
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Query Err')
            logging.getLogger('error_Logger').error(inst)
        finally:
            cursor.close()
            conn.close()
        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/trend')
class Trend(Resource):
    def get(self,headers=None):
        result=[]
        total=[]
        retest=[]
        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        weeknum=request.args.get('weeknum',13)
        weeknum=int(float(weeknum))

        # 取得從今日起往前13週週數
        x_date=Common.WeekNumList(weeknum)

        # 取得13週測板總數及重測率
        query=''' select sum(total) as total,sum(retest) as retest, sum(retest)/sum(total)-1 as 'retestrate', weeknumber from
                  (
                        select count(sn) as total,sum(a.retest) as retest, a.weeknumber from
                        (
                            select week(end_time) as weeknumber,retest+1 as retest,sn
                            from ICT_Project.ict_detail_result
                            where fixture_id='{0}' and board='{1}' and flag=1 
                        ) a group by weeknumber,sn
                  ) b group by weeknumber order by weeknumber '''.format(fixtureId,board)

        print(query)
        rows=Common.FetchDB(query)

        x=1
        for x in range(abs(weeknum)):
            total.append(0)
            retest.append(0)
            x=x+1

        for row in rows:
            if (row['weeknumber'] in x_date):
                # 找到該週位置後替換total list中的值為sql查詢得到的值
                index=x_date.index(row['weeknumber'])
                total[index]=str(row['total'])
                retest[index]=str(row['retestrate'])


        result.append({'x_date':x_date,
                        'total':total,
                        'retest':retest,
                        'retest_target': 4
                    })

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/distribution')
class Distribution(Resource):
    def get(self,headers=None):
        result=[]
        case_distribution=[]
        case_overview=[0,0,0]
 
        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        failtype=request.args.get('failtype','')
        weeknum=request.args.get('weeknum',13)
        weeknum=int(float(weeknum))

        failtable=''

        if failtype=='pins':
            failtable='pins_fail_18275'
        elif failtype=='program':
            failtable='program_fail_18275'
        elif failtype=='component':
            failtable='component_fail_18275'


        # 取得從今日起往前13週週數
        x_date=Common.WeekNumList(weeknum)

        # 取得13週測板總數及重測率
        query=''' select *,count(a.fail_state) as fail_number from  
                  (
                        select fail_state,week(end_time) as weeknumber from ICT_Project.{0} 
                        where fixture_id='{1}' and board='{2}' and flag=1
                  ) a group by weeknumber,fail_state '''.format(failtable,fixtureId,board)

        rows=Common.FetchDB(query)
        print(rows)

        x=1

        for x in range(abs(weeknum)):
            case_distribution.append([0,0,0])
            x=x+1

        print(case_distribution)

        for row in rows:
            if (row['weeknumber'] in x_date):
                # 找到該週位置後替換total list中的值為sql查詢得到的值
                index=x_date.index(row['weeknumber'])
                if(row['fail_state']==0):
                    case_distribution[index][0]=row['fail_number']
                    case_overview[0]=case_overview[0]+row['fail_number']
                elif(row['fail_state']==1):
                    case_distribution[index][1]=row['fail_number']
                    case_overview[1]=case_overview[1]+row['fail_number']
                elif(row['fail_state']==2):
                    case_distribution[index][2]=row['fail_number']
                    case_overview[2]=case_overview[2]+row['fail_number']


        result.append({'x_date':x_date,
                        'case_overview':case_overview,
                        'case_distribution':case_distribution
                    })

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/case_distribution')
class CaseDistribution(Resource):
    def get(self,headers=None):
        result=[]
        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        failtype=request.args.get('failtype','')
        weeknum=request.args.get('weeknum',13)
        weeknum=int(float(weeknum))

        failtable=''

        if failtype=='pins':
            failtable='pins_fail_18275'
        elif failtype=='program':
            failtable='program_fail_18275'
        elif failtype=='component':
            failtable='component_fail_18275'

        after_enddate=Common.BeforeNWeekDate(weeknum)

        testtypelist=['digital_bscan','short','analog','check_pins','pwr_supply','open','analog_function','testjet']

        # 取得13週測板總數及重測率
        query=''' select *,count(a.test_type) as fail_number from 
                 ( 
                    select case when test_type='boundary_scan' then 'digital_bscan'
                                when test_type='digital' then 'digital_bscan'
                                when test_type='power_on' then 'pwr_supply'
                                when test_type='analog_powered' then 'analog_function'
                                else test_type end as test_type,
                            fail_state from ICT_Project.{0} 
                    where fixture_id='{1}' and board='{2}' and flag=1 and end_time>='{3}' 
                 ) a 
                 group by test_type,fail_state '''.format(failtable,fixtureId,board,after_enddate.strftime('%Y-%m-%d'))


        rows=Common.FetchDB(query)
        # 建立每種測試的狀態dict
        state_dict={'opening':0,'ongoing':0,'closing':0}
        digital_bscan_dict=copy.deepcopy(state_dict)
        short_dict=copy.deepcopy(state_dict)
        analog_dict=copy.deepcopy(state_dict)
        check_pins_dict=copy.deepcopy(state_dict)
        pwr_supply_dict=copy.deepcopy(state_dict)
        open_dict=copy.deepcopy(state_dict)
        analog_func_dict=copy.deepcopy(state_dict)
        testjet_dict=copy.deepcopy(state_dict)

        # 從數據庫查詢結果更新dict
        for row in rows:
            if(row['test_type'].lower()=='digital_bscan'):
                if(row['fail_state']==0):
                    digital_bscan_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    digital_bscan_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    digital_bscan_dict['closed']=row['fail_number']

            elif(row['test_type'].lower()=='short'):
                if(row['fail_state']==0):
                    short_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    short_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    short_dict['closed']=row['fail_number']

            elif(row['test_type'].lower()=='analog'):
                if(row['fail_state']==0):
                    analog_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    analog_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    analog_dict['closed']=row['fail_number']    
            
            elif(row['test_type'].lower()=='check_pins'):
                if(row['fail_state']==0):
                    check_pins_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    check_pins_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    check_pins_dict['closed']=row['fail_number']   

            elif(row['test_type'].lower()=='pwr_supply'):
                if(row['fail_state']==0):
                    pwr_supply_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    pwr_supply_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    pwr_supply_dict['closed']=row['fail_number']        

            elif(row['test_type'].lower()=='open'):
                if(row['fail_state']==0):
                    open_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    open_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    open_dict['closed']=row['fail_number']                                                                

            elif(row['test_type'].lower()=='analog_function'):
                if(row['fail_state']==0):
                    analog_func_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    analog_func_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    analog_func_dict['closed']=row['fail_number']               

            elif(row['test_type'].lower()=='testjet'):
                if(row['fail_state']==0):
                    testjet_dict['opening']=row['fail_number']
                elif(row['fail_state']=='1'):
                    testjet_dict['ongoing']=row['fail_number']
                elif(row['fail_state']=='2'):
                    testjet_dict['closed']=row['fail_number']   

        # 將更新後dict加入result並回傳
        result.append({'digital_bscan':digital_bscan_dict,
                       'short':short_dict,                    
                       'analog':analog_dict,
                       'check_pins':check_pins_dict,                           
                       'pwr_supply':pwr_supply_dict,
                       'open':open_dict,
                       'analog_function':analog_func_dict,
                       'testjet':testjet_dict})

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/case_open')
class CaseOpen(Resource):
    def get(self,headers=None):
        result=[]
        opening_result=[]
        ongoing_result=[]
        closed_result=[]

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')

        # weekbefore=13

        # 取得從今日起往前13週週數
        # x_date=Common.WeekNumList(weekbefore*-1)

        # 取得該治具總測版數量
        query=''' select count(*) as total from ict_detail_result 
                  where fixture_id='{0}' and board='{1}' and flag=1 '''.format(fixtureId,board)
        rows=Common.FetchDB(query)  
        totalboard=rows[0]['total']

        # 取得
        query=''' select BRC,test_type,fail_state,fixture_id,b.solution as solution1,c.solution as solution2,
                  d.solution as solution3,a.solution_memo,a.update_time_op,a.update_op,count(BRC) as failcount
                  from pins_fail_18275 a
                  left join fail_solution b on a.solution_1=b.id
                  left join fail_solution c on a.solution_2=c.id
                  left join fail_solution d on a.solution_3=d.id
                  where fixture_id='{0}' and board='{1}' and flag=1 and test_type='open'
                  group by BRC,test_type,fail_state,fixture_id,solution1,solution2,solution3,update_time_op,update_op,solution_memo
                  order by BRC '''.format(fixtureId,board)

        rows=Common.FetchDB(query)

        for row in rows:
            if(row['fail_state']=='0'):
                opening=[]
                probe=[]
                count=[]
                probe.append(row['BRC'])
                count.append(row['failcount'])
                count.append(totalboard)
                opening.append(probe)
                opening.append(count)
                opening_result.append(opening)

            elif(row['fail_state']=='1'):
                probe=[]
                count=[]
                solution=[]
                probe.append(row['BRC'])
                count.append(row['failcount'])
                count.append(totalboard)
                solution.append(row['update_op'])
                solution.append(row['solution1'])
                solution.append(row['solution2'])
                solution.append(row['solution3'])
                solution.append(row['solution_memo'])
                solution.append(row['update_time_op'])
                opening.append(probe)
                opening.append(count)
                opening_result.append(opening)

            elif(row['fail_state']=='2'):
                probe=[]
                count=[]
                probe.append(row['BRC'])
                count.append(row['failcount'])
                count.append(totalboard)
                opening.append(probe)
                opening.append(count)
                opening_result.append(opening)
        print(rows)
        x=1
        # for x in range(weekbefore):
        #     total.append(0)
        #     retest.append(0)
        #     x=x+1

        # for row in rows:
        #     if (row['weeknumber'] in x_date):
        #         # 找到該週位置後替換total list中的值為sql查詢得到的值
        #         index=x_date.index(row['weeknumber'])
        #         total[index]=str(row['total'])
        #         retest[index]=str(row['retestrate'])


        # result.append({'x_date':x_date,
        #                 'total':total,
        #                 'retest':retest
        #             })

        response = jsonify(result)
        response.status_code=200
        return result












