#!/usr/bin/python
# -*- coding:utf-8 -*-
import importlib,sys

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
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

@restapi.resource('/bu_fail')
class PinsDetail(Resource):
    def get(self, headers=None):
        result = []
        try:
            bulist=['MFGI','MFGII','MFGIII','MFGV','MFGVI','MFGVII','MFGVIII']
            dict_pins={}
            dict_prog={}
            dict_comp={}
            pinstotal=0
            progtotal=0
            comptotal=0
        
            # get fail count of BU
            query = ''' select BU,count(*) as 'count' , 'pins' as 'type' from ICT_Project_Test_Realtime.pins_fail group by BU union
                        select BU,count(*) as 'count' ,'prog' as 'type' from ICT_Project_Test_Realtime.program_fail group by BU union
                        select BU,count(*) as 'count' ,'comp' as 'type' from ICT_Project_Test_Realtime.component_fail group by BU '''
        
            rows=Common.FetchDB(query)

            for row in rows:
                if row['type']=='pins':
                    dict_pins[row['BU']]=row['count']
                    pinstotal=pinstotal+row['count']
                if row['type']=='prog':
                    dict_prog[row['BU']]=row['count']
                    progtotal=progtotal+row['count']
                if row['type']=='comp':
                    dict_comp[row['BU']]=row['count']    
                    comptotal=comptotal+row['count']                                               

            for item in bulist:
                totalfailpin=dict_pins[item]/pinstotal
                totalfailprog=dict_pins[item]/progtotal
                comptotalfail=dict_pins[item]/comptotal
                weekfail=[0,0,0,0,0,0,0]
                result.append({
                    'bu':item,
                    'totalfailpin':dict_pins[item]/pinstotal,
                    'totalfailprog':dict_prog[item]/progtotal,
                    'totalfailcomp':dict_comp[item]/comptotal,
                    'weekfail':weekfail
                    })



        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins_fail_detail')
class PinsDetail(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        fixtureId = request.args.get('fixtureId','')
        BU = request.args.get('BU','')

        Next = False        #判斷有沒有上一個參數
        
        query = '''select a.fixture_id,a.bu,a.board,a.program_id,a.totalfailsn,b.totalpin,a.totalfailpin from 
            (
             select fixture_id,bu,board,program_id,count(distinct sn) as totalfailsn,count(distinct BRC) as totalfailpin from ICT_Project_Test_Realtime.pins_fail where 
             '''

        if fromTime!='' and endTime!='' :
            
            query = query + '''end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
            Next = True
        if fixtureId!='' :
            if Next is True:
                query = query + ' AND '
            
            query = query + '''fixture_id = '{0}' '''.format(fixtureId)
            Next = True
        if BU != '' :
            if Next is True:
                query = query + ' AND '
            
            query = query + '''bu = '{0}' '''.format(BU)
            Next = True

        if Next is False:
            query=query+' 1 '


        sql = query + ''' group by fixture_id,bu,board,program_id
            ) a
            inner join 
            (
             select count(distinct node) as totalpin,board from ICT_Project_Test_Realtime.fixture where board='73-18275-04' group by board 
            ) b on a.board=b.board order by fixture_id
            '''
        print(sql)

        try:
            rows=Common.FetchDB(sql)
            print(rows)
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'fixture_id': row['fixture_id'],
                        'BU': row['bu'],
                        'board': row['board'],
                        'program_id': row['program_id'],
                        'totalfailsn': row['totalfailsn'],
                        'totalpin': row['totalpin'],
                        'totalfailpin': row['totalfailpin'],
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins_fail_detail_barchart')
class PinsDetailBarChart(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        fixtureId = request.args.get('fixtureId','')

        Next = False        #判斷有沒有上一個參數
        
        query = '''select a.bu,sum(a.totalfailpin) as totalfailpin  from
            (
             select fixture_id,bu,board,program_id,count(distinct sn) as totalfailsn,count(distinct BRC) as totalfailpin from ICT_Project_Test_Realtime.pins_fail where 
             '''

        if fromTime!='' and endTime!='' :
            
            query = query + '''end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)
            Next = True
        if fixtureId!='' :
            if Next is True:
                query = query + ' AND '
            
            query = query + '''fixture_id = '{0}' '''.format(fixtureId)
            Next = True

        if Next is False:
            query=query+' 1 '


        sql = query + ''' group by fixture_id,bu,board,program_id) a '''
        print(sql)

        try:
            rows=Common.FetchDB(sql)
            print(rows)
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'bu': row['bu'],
                        'totalfailpin': str(row['totalfailpin'])
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

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
        cursor.execute("select distinct(fixture_id) from ICT_Project_Test_Realtime.pins_fail order by fixture_id LIMIT 1 ")
        default_fixtureId=cursor.fetchall()
        cursor.close()
        conn.close()

        fixtureId = request.args.get('fixtureID',default_fixtureId[0]['fixture_id'])
        
        query = '''select b.x,b.y,a.node,a.fixture_id,a.BRC from ICT_Project_Test_Realtime.pins_fail a
                    inner join fixture b on a.node=b.node 
                    where b.board='73-18275-04' '''

        if fromTime!='' and endTime!='' :
            query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)

        if fixtureId!='' :  
            query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        sql = query + ''' group by b.x,b.y,a.node,a.fixture_id order by fixture_id'''
        print(sql)

        try:
            rows=Common.FetchDB(sql)
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
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/passnode')
class PassNode(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        fromTime = request.args.get('startTime','')
        endTime = request.args.get('endTime','')
        
        conn = mysql2.connect()
        cursor = conn.cursor()
        cursor.execute("select distinct(fixture_id) from ICT_Project_Test_Realtime.pins_fail order by fixture_id LIMIT 1 ")
        default_fixtureId=cursor.fetchall()
        cursor.close()
        conn.close()
        
        fixtureId = request.args.get('fixtureID',default_fixtureId[0]['fixture_id'])
        
        query = '''select node,x,y,pins as BRC from fixture where node NOT in
                    (   select distinct(a.node) from  ICT_Project_Test_Realtime.pins_fail  a
                        inner join fixture b on a.node=b.node
                        where a.board='73-18275-04' '''

        if fromTime!='' and endTime!='' :
            query = query + ''' AND end_time BETWEEN '{0}' AND '{1}' '''.format(fromTime,endTime)

        if fixtureId!='' :  
            query = query + ''' AND fixture_id = '{0}' '''.format(fixtureId)

        sql = query + ''' ) and board='73-18275-04' group by node,x,y '''
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

@restapi.resource('/allnode')
class AllNode(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        board = request.args.get('board','73-18275-04')
        
        sql = ''' select x,y,node from ICT_Project_Test_Realtime.fixture  
                    where board='{0}' 
                    group by x,y,node '''.format(board)

        try:
            rows=Common.FetchDB(sql)
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'node': row['node'],
                        'x': row['x'],
                        'y': row['y']
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/failfixture')
class FailFixture(Resource):

    def get(self, headers=None):
        result = []

        # 取得request參數
        # board = request.args.get('board','73-18275-04')
        
        sql = ''' select distinct(fixture_id) from ICT_Project_Test_Realtime.pins_fail '''

        try:
            rows=Common.FetchDB(sql)
            # data exist
            if len(rows)>0:
                for row in rows:
                    result.append({
                        'fixture_id': row['fixture_id']
                    })
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/board')
class Board(Resource):
    def get(self, headers=None):
        result = ''

        # 取得request參數
        board = request.args.get('board','73-18275-04')
        
        sql = ''' select x,y from ICT_Project_Test_Realtime.board  
                    where board='{0}' 
                    group by x,y'''.format(board)

        try:
            rows=Common.FetchDB(sql)
            # data exist
            if len(rows)>0:
                for row in rows:
                    result={
                        'x': row['x'],
                        'y': row['y']
                    }
        except Exception as inst:
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)


        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins_fail')
class PinsFail(Resource):
    def get(self, headers=None):

        pins = 0
        comp = 0
        prog = 0
        totals = []
        result = ''
        sql = '''select count(DISTINCT seq) as pins from ICT_Project_Test_Realtime.pins_fail
        UNION
        select count(DISTINCT seq) as comp from ICT_Project_Test_Realtime.component_fail
        UNION
        select count(DISTINCT seq) as prog from ICT_Project_Test_Realtime.program_fail
        '''

        try:
            rows=Common.FetchDB(sql)
            # data exist
            if len(rows)>0:
                for row in rows:
                    totals.append(row['pins'])
            pins = totals[0]
            comp = totals[1]
            prog = totals[2]
            total = pins + comp + prog
            result={
                'pins_failrate': '{:.2}'.format(pins / total)
                }
        except Exception as inst:
            logging.getLogger('error_Logger').error('Pins Fail Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result



@restapi.resource('/boardfixture')
class BoardFixture(Resource):
    def get(self, headers=None):
        result = []

        # 取得request參數
        board = request.args.get('board','')
        
        query = ''' select distinct board,fixture_id from ICT_Project_Test_Realtime.ict_detail_result where fail_code='failed' '''

        if board!='':
            
            query = query + ''' AND board = '{0}' '''.format(board)
        
        sql = query+ ''' group by board,fixture_id,fail_code '''
        
        print(sql)

        try:
            rows=Common.FetchDB(sql)
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
            logging.getLogger('error_Logger').error('ICT Result Err')
            logging.getLogger('error_Logger').error(inst)

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins/trend')
class PinsTrend(Resource):
    def get(self,headers=None):

        total=[]
        retest=[]
        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        weeknum=request.args.get('weeknum',20)
        weeknum=int(float(weeknum))

        # 取得從今日起往前n週週數
        x_date=Common.WeekNumList(weeknum)

        # 取得n週測板總數及重測率
        query=''' select sum(total) as total,sum(retest) as retest, sum(retest)/sum(total)-1 as 'retestrate', weeknumber from
                  (
                        select count(sn) as total,sum(a.retest) as retest, a.weeknumber from
                        (
                            select week(end_time) as weeknumber,retest+1 as retest,sn
                            from ICT_Project_Test_Realtime.ict_detail_result
                            where fixture_id='{0}' and board='{1}'  
                            group by sn
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
                total[index]=float(row['total'])
                retest[index]=float(row['retestrate'])


        result=({'payload':
                    {   
                        'x_date':x_date,
                        'total':total,
                        'retest':retest,
                        'retest_target': 4
                    }
                })

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins/distribution')
class PinsDistribution(Resource):
    def get(self,headers=None):

        case_distribution=[]
        case_overview=[0,0,0]
 
        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        weeknum=request.args.get('weeknum',20)
        weeknum=int(float(weeknum))


        # 取得從今日起往前13週週數
        x_date=Common.WeekNumList(weeknum)

        after_enddate=Common.BeforeNWeekDate(weeknum)

        # 取得13週測板總數及重測率
        query='''select weeknumber,count(a.component) as fail_number,fail_state from  
                (
                    select component,fail_state,week(end_time) as weeknumber,test_type from ICT_Project_Test_Realtime.pins_fail
                    where fixture_id='{0}' and board='{1}' and end_time>='{2}' 
                    and flag=1 and test_type in ('digital','boundary scan','analog powered','powercheck','analog')
                    group by component,weeknumber,fail_state
                ) a group by weeknumber,fail_state
                union
                select weeknumber,count(a.component) as fail_number,fail_state from  
                (
                    select concat(component,'/',pins) as component,fail_state,week(end_time) as weeknumber,test_type from ICT_Project_Test_Realtime.pins_fail
                    where fixture_id='{0}' and board='{1}' and end_time>='{2}' 
                    and flag=1 and test_type = 'testjet'
                    group by component,weeknumber,pins,fail_state
                ) a group by weeknumber,fail_state
                union
                select weeknumber,count(a.component) as fail_number,fail_state from  
                (
                    select BRC as component,fail_state,week(end_time) as weeknumber,test_type,update_time_op from ICT_Project_Test_Realtime.pins_fail
                    where fixture_id='{0}' and board='{1}' and end_time>='{2}' 
                    and flag=1 and test_type in ('open','short')
                    group by BRC,fail_state,weeknumber
                ) a group by fail_state,weeknumber '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))

        rows=Common.FetchDB(query)
        print(rows)
        x=0

        for x in range(abs(weeknum)):
            case_distribution.append([0,0,0])
            x=x+1

        for row in rows:

            if (row['weeknumber'] in x_date):
                # 找到該週位置後替換total list中的值為sql查詢得到的值
                index=x_date.index(row['weeknumber'])
                if(row['fail_state']==0):
                    case_distribution[index][0]=row['fail_number']
                    case_overview[0]=case_overview[0]+row['fail_number']
                    print(case_overview[0])
                elif(row['fail_state']==1):
                    case_distribution[index][1]=row['fail_number']
                    case_overview[1]=case_overview[1]+row['fail_number']
                elif(row['fail_state']==2):
                    case_distribution[index][2]=row['fail_number']
                    case_overview[2]=case_overview[2]+row['fail_number']


        result=({'payload':
                    {
                        'x_date':x_date,
                        'case_overview':case_overview,
                        'case_distribution':case_distribution
                    }
                })

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins/case_distribution')
class PinsCaseDistribution(Resource):
    def get(self,headers=None):

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        weeknum=request.args.get('weeknum',20)
        weeknum=int(float(weeknum))


        after_enddate=Common.BeforeNWeekDate(weeknum)

        testtypelist=['digital_bscan','short','analog','pwr_supply','open','analog_function','testjet']

        # 取得n週測板總數及重測率
        query='''   select case when test_type='boundary scan' then 'digital_bscan'
                    when test_type='digital' then 'digital_bscan'
                    else test_type end as test_type,fail_state,fail_number from
                    (
                        select count(a.component) as fail_number,test_type,fail_state from  
                        (
                            select component,fail_state,
                            case when test_type='powercheck' then 'pwr_analog'
                            when test_type='analog powered' then 'pwr_analog'
                            else test_type end as test_type                        
                            from ICT_Project_Test_Realtime.pins_fail
                            where fixture_id='{0}' and board='{1}' and end_time>='{2}'  
                            and flag=1 and test_type in ('digital','boundary scan','analog powered','powercheck','analog')
                            group by component,fail_state
                        ) a group by fail_state,test_type
                        union
                        select count(a.component) as fail_number,test_type,fail_state from  
                        (
                            select concat(component,'/',pins) as component,fail_state,test_type from ICT_Project_Test_Realtime.pins_fail
                            where fixture_id='{0}' and board='{1}' and end_time>='{2}'  
                            and flag=1 and test_type = 'testjet'
                            group by component,pins,fail_state
                        ) a group by fail_state,test_type
                        union
                        select count(a.component) as fail_number,test_type,fail_state from  
                        (
                            select BRC as component,fail_state,test_type,update_time_op from ICT_Project_Test_Realtime.pins_fail
                            where fixture_id='{0}' and board='{1}' and end_time>='{2}'  
                            and flag=1 and test_type in ('open','short')
                            group by BRC,fail_state
                        ) a group by fail_state,test_type
                    ) t '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))

        print(query)

        rows=Common.FetchDB(query)
        # 建立每種測試的狀態dict
        state_dict={'opening':0,'ongoing':0,'closed':0}
        digital_bscan_dict=copy.deepcopy(state_dict)
        short_dict=copy.deepcopy(state_dict)
        analog_dict=copy.deepcopy(state_dict)
        pwr_analog_dict=copy.deepcopy(state_dict)
        open_dict=copy.deepcopy(state_dict)
        testjet_dict=copy.deepcopy(state_dict)

        # 從數據庫查詢結果更新dict
        for row in rows:
            if(row['test_type'].lower()=='digital_bscan'):
                if(row['fail_state']==0):
                    digital_bscan_dict['opening']=row['fail_number']
                elif(row['fail_state']==1):
                    digital_bscan_dict['ongoing']=row['fail_number']
                elif(row['fail_state']==2):
                    digital_bscan_dict['closed']=row['fail_number']

            elif(row['test_type'].lower()=='short'):
                if(row['fail_state']==0):
                    short_dict['opening']=row['fail_number']
                elif(row['fail_state']==1):
                    short_dict['ongoing']=row['fail_number']
                elif(row['fail_state']==2):
                    short_dict['closed']=row['fail_number']

            elif(row['test_type'].lower()=='analog'):
                if(row['fail_state']==0):
                    analog_dict['opening']=row['fail_number']
                elif(row['fail_state']==1):
                    analog_dict['ongoing']=row['fail_number']
                elif(row['fail_state']==2):
                    analog_dict['closed']=row['fail_number']    
            

            elif(row['test_type'].lower()=='pwr_analog'):
                if(row['fail_state']==0):
                    pwr_analog_dict['opening']=row['fail_number']
                elif(row['fail_state']==1):
                    pwr_analog_dict['ongoing']=row['fail_number']
                elif(row['fail_state']==2):
                    pwr_analog_dict['closed']=row['fail_number']        

            elif(row['test_type'].lower()=='open'):
                if(row['fail_state']==0):
                    open_dict['opening']=row['fail_number']
                elif(row['fail_state']==1):
                    open_dict['ongoing']=row['fail_number']
                elif(row['fail_state']==2):
                    open_dict['closed']=row['fail_number']                                                                            

            elif(row['test_type'].lower()=='testjet'):
                if(row['fail_state']==0):
                    testjet_dict['opening']=row['fail_number']
                elif(row['fail_state']==1):
                    testjet_dict['ongoing']=row['fail_number']
                elif(row['fail_state']==2):
                    testjet_dict['closed']=row['fail_number']   

        # 將更新後dict加入result並回傳
        result=({'payload':
                    {
                        'digital_bscan':digital_bscan_dict,
                        'short':short_dict,                    
                        'analog':analog_dict,                         
                        'pwr_analog':pwr_analog_dict,
                        'open':open_dict,
                        'testjet':testjet_dict
                    }
                })

        response = jsonify(result)
        response.status_code=200
        return result

@restapi.resource('/pins/case_openshort')
class PinsCaseOpenShort(Resource):
    def get(self,headers=None):
        board_list=[]
        beforefail_dict={}
        beforetotal_dict={}
        afterfail_dict={}
        aftertotal_dict={}
        count_dict={}

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')
        testtype= request.args.get('testtype','')

        try:
            after_enddate=Common.BeforeNWeekDate(20)
            
            # 取得該治具總測板數量
            board_list=Common.GetTotalBoardByFixture(fixtureId,board)
            totalboard=len(board_list)
            
            # 取得每個BRC最新closed時間
            rows=Common.GetClosedTimeByFixture(fixtureId,board,testtype) 
            
            for row in rows:
                beforetotal=0
                aftertotal=0
                for item in board_list:
                    if(item['end_time']>=row['update_time']):
                        aftertotal=aftertotal+1
                    else:
                        beforetotal=beforetotal+1

                beforetotal_dict[row['BRC']]=beforetotal
                aftertotal_dict[row['BRC']]=aftertotal
            
            # 取得為維護後重測次數(fail_state不為closed)
            rows=Common.GetAfterFailCountByFixture(fixtureId,board,testtype)
            for row in rows:
                afterfail_dict[row['BRC']]=row['failcount']

            # 取得為維護前重測次數(fail_state為closed)            
            rows=Common.GetBeforeFailCountByFixture(fixtureId,board,testtype)
            for row in rows:
                beforefail_dict[row['BRC']]=row['failcount']    

            # 取得每次closed後重新open次數
            rows=Common.GetReopenCountByFixture(fixtureId,board,testtype)
            for row in rows:
                count_dict[row['BRC']]=row['reopencount']   

            query=''' select BRC,test_type,fail_state,fixture_id,b.solution as solution1,c.solution as solution2,
                      d.solution as solution3,a.solution_memo,max(a.update_time_op) as update_time_op,a.update_op,count(BRC) as failcount
                      from ICT_Project_Test_Realtime.pins_fail a
                      left join fail_solution b on a.solution_1=b.id 
                      left join fail_solution c on a.solution_2=c.id 
                      left join fail_solution d on a.solution_3=d.id 
                      where fixture_id='{0}' and board='{1}' and flag=1 and test_type='{2}' and end_time>='{3}'  
                      group by BRC,test_type,fail_state,fixture_id,solution1,solution2,solution3,update_op,solution_memo
                      order by BRC '''.format(fixtureId,board,testtype,after_enddate.strftime('%Y-%m-%d'))

            rows=Common.FetchDB(query)

            result=Common.GetCaseBRCDetail(rows,count_dict,beforefail_dict,beforetotal_dict,afterfail_dict,aftertotal_dict,totalboard,testtype)


            response = jsonify(result)
            response.status_code=200
            return result
        except Exception as err:
            print("[error]: {0}".format(err))

@restapi.resource('/pins/case_testjet')
class PinsCaseTestjet(Resource):
    def get(self,headers=None):
        board_list=[]
        beforefail_dict={}
        beforetotal_dict={}
        afterfail_dict={}
        aftertotal_dict={}
        count_dict={}

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')

        try:
            after_enddate=Common.BeforeNWeekDate(20)

            # 取得該治具總測板數量
            board_list=Common.GetTotalBoardByProgram(fixtureId,board)
            totalboard=len(board_list)
            
            # 取得每個component/pins最新closed時間
            query=''' select concat(component,'/',pins) as component,max(update_time_op) as update_time from ICT_Project_Test_Realtime.pins_fail
                      where fixture_id='{0}' and board='{1}' and flag=1 and end_time>='{2}'  
                      and fail_state=2 and test_type='testjet' group by component,pins '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))
            rows=Common.FetchDB(query)  
            
            for row in rows:
                beforetotal=0
                aftertotal=0
                for item in board_list:
                    if(item['end_time']>=row['update_time']):
                        aftertotal=aftertotal+1
                    else:
                        beforetotal=beforetotal+1

                beforetotal_dict[row['component']]=beforetotal
                aftertotal_dict[row['component']]=aftertotal


            # 取得為維護後重測次數(fail_state不為closed)
            query=''' select count(component) as failcount,component from
                      (
                        select concat(component,'/',pins) as component from ICT_Project_Test_Realtime.pins_fail
                        where  fixture_id='{0}' and board='{1}' and flag=1 and end_time>='{2}'  
                        and fail_state between 0 and 1  and test_type='testjet'
                      ) a
                      group by component '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))
            rows=Common.FetchDB(query)
            for row in rows:
                afterfail_dict[row['component']]=row['failcount']
            
            # 取得維護前重測次數(fail_state為closed)
            query=''' select count(component) as failcount,component from
                      (
                        select concat(component,'/',pins) as component from ICT_Project_Test_Realtime.pins_fail
                        where  fixture_id='{0}' and board='{1}'  and flag=1 and end_time>='{2}'  
                        and fail_state = 2  and test_type='testjet'
                       ) a
                      group by component '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))
            rows=Common.FetchDB(query)
            for row in rows:
                beforefail_dict[row['component']]=row['failcount']    

            # 取得每次closed後重新open次數
            query=''' select count(component) as reopencount,component from
                     (
                        select concat(component,'/',pins) as component,update_time_op from ICT_Project_Test_Realtime.pins_fail
                        where fixture_id='{0}' and board='{1}' and flag=1 and end_time>='{2}'  
                        and test_type='testjet' and fail_state=2  
                        group by component,pins,update_time_op
                     ) a group by component,update_time_op '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))    
            rows=Common.FetchDB(query)
            for row in rows:
                count_dict[row['component']]=row['reopencount']   

            query=''' select concat(component,'/',pins) as component,test_type,fail_state,fixture_id,b.solution as solution1,c.solution as solution2,
                      d.solution as solution3,a.solution_memo,max(a.update_time_op) as update_time_op,a.update_op,count(component) as failcount
                      from ICT_Project_Test_Realtime.pins_fail a
                      left join ICT_Project_Test_Realtime.fail_solution b on a.solution_1=b.id
                      left join ICT_Project_Test_Realtime.fail_solution c on a.solution_2=c.id
                      left join ICT_Project_Test_Realtime.fail_solution d on a.solution_3=d.id
                      where fixture_id='{0}' and board='{1}' and flag=1 and end_time>='{2}'  and test_type='testjet'
                      group by component,pins,test_type,fail_state,fixture_id,solution1,solution2,solution3,update_op,solution_memo
                      order by component,pins  '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))
            
            rows=Common.FetchDB(query)

            result=Common.GetCaseCompDetail(rows,count_dict,beforefail_dict,beforetotal_dict,afterfail_dict,aftertotal_dict,totalboard,'testjet')

            response = jsonify(result)
            response.status_code=200
            return result
        except Exception as err:
            print("[error]: {0}".format(err))

@restapi.resource('/pins/case_digital')
class PinsCaseDigital(Resource):
    def get(self,headers=None):
        board_list=[]
        beforefail_dict={}
        beforetotal_dict={}
        afterfail_dict={}
        aftertotal_dict={}
        count_dict={}
        testtype='digital'

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')

        try:
            after_enddate=Common.BeforeNWeekDate(20)
            # 取得該治具總測板數量
            board_list=Common.GetTotalBoardByFixture(fixtureId,board)
            totalboard=len(board_list)
            
            # 取得每個component最新closed時間
            rows=Common.GetClosedTimeByFixture(fixtureId,board,testtype)
            
            for row in rows:
                beforetotal=0
                aftertotal=0
                for item in board_list:
                    if(item['end_time']>=row['update_time']):
                        aftertotal=aftertotal+1
                    else:
                        beforetotal=beforetotal+1

                beforetotal_dict[row['component']]=beforetotal
                aftertotal_dict[row['component']]=aftertotal

            # 取得為維護後重測次數(fail_state不為closed)
            rows=Common.GetAfterFailCountByFixture(fixtureId,board,testtype)            
            for row in rows:
                afterfail_dict[row['component']]=row['failcount']
            
            # 取得維護前重測次數(fail_state為closed)
            rows=Common.GetBeforeFailCountByFixture(fixtureId,board,testtype)
            for row in rows:
                beforefail_dict[row['component']]=row['failcount']    

            # 取得每次closed後重新open次數
            rows=Common.GetReopenCountByFixture(fixtureId,board,testtype)
            for row in rows:
                count_dict[row['component']]=row['reopencount']   

            # 取得明細顯示資料 
            query=''' select component,test_type,fail_state,fixture_id,b.solution as solution1,c.solution as solution2,
                      d.solution as solution3,a.solution_memo,max(a.update_time_op) as update_time_op,a.update_op,count(component) as failcount
                      from ICT_Project_Test_Realtime.pins_fail a
                      left join ICT_Project_Test_Realtime.fail_solution b on a.solution_1=b.id
                      left join ICT_Project_Test_Realtime.fail_solution c on a.solution_2=c.id
                      left join ICT_Project_Test_Realtime.fail_solution d on a.solution_3=d.id
                      where fixture_id='{0}' and board='{1}' and flag=1  and end_time>='{2}'  and test_type in ('digital','boundary scan')
                      group by component,test_type,fail_state,fixture_id,solution1,solution2,solution3,update_op,solution_memo
                      order by component  '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))           
            rows=Common.FetchDB(query)

            result=Common.GetCaseCompDetail(rows,count_dict,beforefail_dict,beforetotal_dict,afterfail_dict,aftertotal_dict,totalboard,testtype)

            response = jsonify(result)
            response.status_code=200
            return result
        except Exception as err:
            print("[error]: {0}".format(err))

@restapi.resource('/pins/case_analog_function')
class PinsCaseAnalogFunction(Resource):
    def get(self,headers=None):
        board_list=[]
        beforefail_dict={}
        beforetotal_dict={}
        afterfail_dict={}
        aftertotal_dict={}
        count_dict={}
        testtype='analog_function'

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')

        try:
            after_enddate=Common.BeforeNWeekDate(20)

            # 取得該治具總測板數量
            board_list=Common.GetTotalBoardByFixture(fixtureId,board)
            totalboard=len(board_list)

            # 取得每個component最新closed時間
            rows=Common.GetClosedTimeByFixture(fixtureId,board,testtype)  

            for row in rows:
                beforetotal=0
                aftertotal=0
                for item in board_list:
                    if(item['end_time']>=row['update_time']):
                        aftertotal=aftertotal+1
                    else:
                        beforetotal=beforetotal+1

                beforetotal_dict[row['component']]=beforetotal
                aftertotal_dict[row['component']]=aftertotal

            # 取得為維護後重測次數(fail_state不為closed)
            rows=Common.GetAfterFailCountByFixture(fixtureId,board,testtype)            
            for row in rows:
                afterfail_dict[row['component']]=row['failcount']
            
            # 取得維護前重測次數(fail_state為closed)
            rows=Common.GetBeforeFailCountByFixture(fixtureId,board,testtype)
            for row in rows:
                beforefail_dict[row['component']]=row['failcount']    

            # 取得每次closed後重新open次數
            rows=Common.GetReopenCountByFixture(fixtureId,board,testtype)
            for row in rows:
                count_dict[row['component']]=row['reopencount']  

            query=''' select component,test_type,fail_state,fixture_id,b.solution as solution1,c.solution as solution2,
                      d.solution as solution3,a.solution_memo,max(a.update_time_op) as update_time_op,a.update_op,count(component) as failcount
                      from ICT_Project_Test_Realtime.pins_fail a
                      left join ICT_Project_Test_Realtime.fail_solution b on a.solution_1=b.id
                      left join ICT_Project_Test_Realtime.fail_solution c on a.solution_2=c.id
                      left join ICT_Project_Test_Realtime.fail_solution d on a.solution_3=d.id
                      where fixture_id='{0}' and board='{1}'  and flag=1  and end_time>='{2}' and test_type in ('analog powered','powercheck')
                      group by component,test_type,fail_state,fixture_id,solution1,solution2,solution3,update_op,solution_memo
                      order by component  '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))
            
            rows=Common.FetchDB(query)

            result=Common.GetCaseCompDetail(rows,count_dict,beforefail_dict,beforetotal_dict,afterfail_dict,aftertotal_dict,totalboard,testtype)

            response = jsonify(result)
            response.status_code=200
            return result
        except Exception as err:
            print("[error]: {0}".format(err))

@restapi.resource('/pins/case_analog')
class PinsCaseAnalog(Resource):
    def get(self,headers=None):
        board_list=[]
        beforefail_dict={}
        beforetotal_dict={}
        afterfail_dict={}
        aftertotal_dict={}
        count_dict={}
        testtype='analog'

        # 取得request參數
        board = request.args.get('board','')
        fixtureId = request.args.get('fixtureId','')

        try:
            after_enddate=Common.BeforeNWeekDate(20)            
            # 取得該治具總測板數量
            board_list=Common.GetTotalBoardByFixture(fixtureId,board)
            totalboard=len(board_list)

            # 取得每個component最新closed時間
            rows=Common.GetClosedTimeByFixture(fixtureId,board,testtype)

            for row in rows:
                beforetotal=0
                aftertotal=0
                for item in board_list:
                    if(item['end_time']>=row['update_time']):
                        aftertotal=aftertotal+1
                    else:
                        beforetotal=beforetotal+1

                beforetotal_dict[row['component']]=beforetotal
                aftertotal_dict[row['component']]=aftertotal

            # 取得為維護後重測次數(fail_state不為closed)
            rows=Common.GetAfterFailCountByFixture(fixtureId,board,testtype)            
            for row in rows:
                afterfail_dict[row['component']]=row['failcount']
            
            # 取得維護前重測次數(fail_state為closed)
            rows=Common.GetBeforeFailCountByFixture(fixtureId,board,testtype)
            for row in rows:
                beforefail_dict[row['component']]=row['failcount']    

            # 取得每次closed後重新open次數
            rows=Common.GetReopenCountByFixture(fixtureId,board,testtype)
            for row in rows:
                count_dict[row['component']]=row['reopencount']  

            query=''' select component,high_limit,low_limit,nominal,test_type,fail_state,fixture_id,b.solution as solution1,c.solution as solution2,
                      d.solution as solution3,a.solution_memo,max(a.update_time_op) as update_time_op,a.update_op,count(component) as failcount
                      from ICT_Project_Test_Realtime.pins_fail a
                      left join ICT_Project_Test_Realtime.fail_solution b on a.solution_1=b.id
                      left join ICT_Project_Test_Realtime.fail_solution c on a.solution_2=c.id
                      left join ICT_Project_Test_Realtime.fail_solution d on a.solution_3=d.id
                      where fixture_id='{0}' and board='{1}'  and flag=1  and end_time>='{2}' and test_type='analog'
                      group by component,test_type,fail_state,fixture_id,solution1,solution2,solution3,update_op,solution_memo
                      order by component  '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))
            print(query)
            rows=Common.FetchDB(query)

            result=Common.GetCaseCompDetail(rows,count_dict,beforefail_dict,beforetotal_dict,afterfail_dict,aftertotal_dict,totalboard,testtype)

            response = jsonify(result)
            response.status_code=200
            return result
        except Exception as err:
            print("[error]: {0}".format(err))


