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
    
    # 取得治具總測板數量
    def GetTotalBoard(fixtureId,board):
        after_enddate=Common.BeforeNWeekDate(20)

        query=''' select sn,max(end_time) as end_time from ict_detail_result 
                  where fixture_id='{0}' and board='{1}' 
                  and flag=1  and end_time>='{2}' group by sn '''.format(fixtureId,board,after_enddate.strftime('%Y-%m-%d'))

        rows=Common.FetchDB(query)  
        return(rows)
    
    # 取得為維護後重測次數(fail_state不為closed)
    def GetAfterFailCount(fixtureId,board,testtype):
        try:
            after_enddate=Common.BeforeNWeekDate(20)
            element='component'

            if(testtype=='analog'):
                testtype=''' ='analog' '''

            elif(testtype=='analog_function'):
                testtype=''' in ('analog_powered','power_on') '''       
            
            elif(testtype=='digital'):
                testtype=''' in ('digital','boundary_scan') '''  

            elif(testtype=='open'):
                testtype=''' ='open' '''
                element='BRC'

            elif(testtype=='short'):
                testtype=''' ='short' '''
                element='BRC'        

            query=''' select count({0}) as failcount,{0} from
                      (
                        select a.{0},update_time_op,maxupdatetime from pins_fail_18275  a
                        inner join 
                        (
                            select {0},max(update_time_op) as maxupdatetime from pins_fail_18275 where fail_state=2 group by {0}
                        )b on a.{0}=b.{0} 
                        where  fixture_id='{1}' and board='{2}' and fail_state between 0 and 1  and flag=1
                        and test_type {3} and (a.update_time_op>b.maxupdatetime) and end_time>='{4}'
                      ) a
                      group by {0} '''.format(element,fixtureId,board,testtype,after_enddate.strftime('%Y-%m-%d'))


            rows=Common.FetchDB(query)       
            return(rows) 

        except Exception as inst:
            print(inst)        

    # 取得為維護前重測次數(fail_state為closed)
    def GetBeforeFailCount(fixtureId,board,testtype):
        try:
            after_enddate=Common.BeforeNWeekDate(20)
            element='component'

            if(testtype=='analog'):
                testtype=''' ='analog' '''

            elif(testtype=='analog_function'):
                testtype=''' in ('analog_powered','power_on') '''       
            
            elif(testtype=='digital'):
                testtype=''' in ('digital','boundary_scan') '''  

            elif(testtype=='open'):
                testtype=''' ='open' '''
                element='BRC'

            elif(testtype=='short'):
                testtype=''' ='short' '''
                element='BRC'        

            query=''' select count({0}) as failcount,{0} from  pins_fail_18275
                      where  fixture_id='{1}' and board='{2}' 
                      and fail_state = 2 and flag=1 and test_type {3} and end_time>='{4}' 
                      group by {0} '''.format(element,fixtureId,board,testtype,after_enddate.strftime('%Y-%m-%d'))


            rows=Common.FetchDB(query)       
            return(rows) 
        except Exception as inst:
            print(inst)                

    # 取得為維護前重測次數(fail_state為closed)
    def GetClosedTime(fixtureId,board,testtype):
        try:
            after_enddate=Common.BeforeNWeekDate(20)
            element='component'

            if(testtype=='analog'):
                testtype=''' ='analog' '''

            elif(testtype=='analog_function'):
                testtype=''' in ('analog_powered','power_on') '''       
            
            elif(testtype=='digital'):
                testtype=''' in ('digital','boundary_scan') '''  

            elif(testtype=='open'):
                testtype=''' ='open' '''
                element='BRC'

            elif(testtype=='short'):
                testtype=''' ='short' '''
                element='BRC'        

            query=''' select {0}, max(update_time_op) as update_time from pins_fail_18275
                      where  fixture_id='{1}' and board='{2}' and fail_state = 2 
                      and flag=1  and test_type {3} and end_time>='{4}' 
                      group by {0} '''.format(element,fixtureId,board,testtype,after_enddate.strftime('%Y-%m-%d'))

            rows=Common.FetchDB(query)       
            return(rows)   

        except Exception as inst:
            print(inst)           

    # 取得為維護前重測次數(fail_state為closed)
    def GetReopenCount(fixtureId,board,testtype):
        try:
            after_enddate=Common.BeforeNWeekDate(20)            
            element='component'

            if(testtype=='analog'):
                testtype=''' ='analog' '''

            elif(testtype=='analog_function'):
                testtype=''' in ('analog_powered','power_on') '''       
            
            elif(testtype=='digital'):
                testtype=''' in ('digital','boundary_scan') '''  

            elif(testtype=='open'):
                testtype=''' ='open' '''
                element='BRC'

            elif(testtype=='short'):
                testtype=''' ='short' '''
                element='BRC'        

            query=''' select count({0}) as reopencount,{0} from  
                      (
                        select {0},update_time_op from pins_fail_18275
                        where fixture_id='{1}' and board='{2}' and test_type {3} and fail_state=2 
                        and flag=1 and end_time>='{4}'  
                        group by {0},update_time_op
                      ) a group by {0},update_time_op '''.format(element,fixtureId,board,testtype,after_enddate.strftime('%Y-%m-%d'))


            rows=Common.FetchDB(query)       
            return(rows)   

        except Exception as inst:
            print(inst)

    def GetCaseCompDetail(rows,count_dict,beforefail_dict,beforetotal_dict,afterfail_dict,aftertotal_dict,totalboard,testtype):
        try:
            if(testtype=='open' or 'short'):
                element='BRC'
            else:
                element='component'
            opening_result=[]
            ongoing_result=[]
            closed_result=[]
            for row in rows:
                if(row['fail_state']==0):
                    opening=[]
                    probe=[]
                    count=[]
                    probe.append(row['component'])
                    opening.append(probe)
                    if(testtype=='analog'):
                        opening.append([str(row['high_limit'])])
                        opening.append([str(row['low_limit'])])
                        opening.append(['' if (row['nominal']) is None else str(row['nominal'])])
                        
                    opening.append([row['failcount']])
                    opening.append([totalboard])
                    if(row['component'] in count_dict):
                        opening.append([[count_dict[row['component']]]+1])
                    else:
                        opening.append([1])
                    opening_result.append(opening)

                elif(row['fail_state']==1):
                    ongoing=[]
                    probe=[]
                    count=[]
                    beforecount=[]
                    aftercount=[]
                    solution=[]

                    probe.append(row['component'])
                    if(testtype=='analog'):
                        count.append(str(row['high_limit']))
                        count.append(str(row['low_limit']))
                        count.append('' if (row['nominal']) is None else str(row['nominal'])) 
                
                    count.append(row['failcount'])
                    count.append(totalboard)

                    if(row['component'] in beforefail_dict):
                        beforecount.append(beforefail_dict[row['component']])
                    else:
                        beforecount.append(0)

                    if(row['component'] in beforetotal_dict):
                        beforecount.append(beforetotal_dict[row['component']])
                    else:
                        beforecount.append(totalboard)

                    if(row['component'] in afterfail_dict):
                        aftercount.append(afterfail_dict[row['component']])
                    else:
                        aftercount.append(0)

                    if(row['component'] in aftertotal_dict):
                        aftercount.append(aftertotal_dict[row['component']])
                    else:
                        aftercount.append(0)

                    solution.append(row['update_op'])
                    solution.append(row['solution1'])
                    solution.append(row['solution2'])
                    solution.append(row['solution3'])
                    solution.append(row['solution_memo'])
                    solution.append(str(row['update_time_op']))
                    if(row['component'] in count_dict):
                        solution.append(count_dict[row['component']])
                    else:
                        solution.append(1)
                    
                    ongoing.append(probe)
                    ongoing.append(count)
                    ongoing.append(beforecount)
                    ongoing.append(aftercount)
                    ongoing.append(solution)

                    ongoing_result.append(ongoing)

                elif(row['fail_state']==2):
                    closed=[]
                    probe=[]
                    count=[]
                    beforecount=[]
                    aftercount=[]
                    solution=[]

                    probe.append(row['component'])

                    if(testtype=='analog'):
                        count.append(str(row['high_limit']))
                        count.append(str(row['low_limit']))
                        count.append('' if (row['nominal']) is None else str(row['nominal']))         
   
                    count.append(row['failcount'])
                    count.append(totalboard)

                    if(row['component'] in beforefail_dict):
                        beforecount.append(beforefail_dict[row['component']])
                    else:
                        beforecount.append(0)

                    if(row['component'] in beforetotal_dict):
                        beforecount.append(beforetotal_dict[row['component']])
                    else:
                        beforecount.append(totalboard)

                    if(row['component'] in afterfail_dict):
                        aftercount.append(afterfail_dict[row['component']])
                    else:
                        aftercount.append(0)
                    
                    if(row['component'] in aftertotal_dict):
                        aftercount.append(aftertotal_dict[row['component']])
                    else:
                        aftercount.append(0)
                    solution.append(row['update_op'])
                    solution.append(row['solution1'])
                    solution.append(row['solution2'])
                    solution.append(row['solution3'])
                    solution.append(row['solution_memo'])
                    solution.append(str(row['update_time_op']))
                    if(row['component'] in count_dict):
                        solution.append(count_dict[row['component']])
                    else:
                        solution.append(1)

                    closed.append(probe)
                    closed.append(count)
                    closed.append(beforecount)
                    closed.append(aftercount)
                    closed.append(solution)

                    closed_result.append(closed)

            result=({'payload':
                        {
                            'opening':opening_result,
                            'ongoing':ongoing_result,
                            'closed':closed_result
                        }
                    })                
            return(result)
        except Exception as inst:
            print(inst)
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











