import flask_restful

from flask_restful import request
from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restful import Resource, Api, reqparse
from app.extensions import mysql2,restapi,cache
import time
import logging
from datetime import date,datetime as dt, timedelta
import codecs, hashlib, os, shutil


app = Flask(__name__)
api = Api(app=app)

@restapi.resource('/newlog_batch/<string:filename>')
class NewlogBatch(Resource):
	def get(self,filename):
		path=os.path.abspath("..")+"newlog/"

		fp = open(path+filename, 'r')

		line = fp.readline()

		path=os.path.abspath("..")+"newlog/"
		fp = open(path+filename, 'r')
		line = fp.readline()
		db_sp=[]
		board=''
		machine=''
		sn=''
		end_time=''

		while line :
			line = line.strip('{\n}')
			sp=line.split(":")

			if (len(sp)==0 or ("=" in sp[0])): break			
			else :
				if (sp[0].strip() == 'Board'):
					board=sp[1].split()[0].strip()
					db_sp.append(board)
				elif (sp[0].strip() == 'Serial_Number'):
					sn=sp[1].strip()
					db_sp.append(sn)
				elif (sp[0].strip() == 'ICT_STATION'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Cell_No'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Status'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Fail_code'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Start_time'):
					strtime=(sp[1]+sp[2]+sp[3]).strip().replace(' ','')
					start_time=dt.strptime(strtime.replace('-',''),'%Y%m%d%H%M%S')
					db_sp.append(start_time)
				elif (sp[0].strip() == 'End_time'):
					strtime=(sp[1]+sp[2]+sp[3]).strip().replace(' ','')
					end_time=dt.strptime(strtime.replace('-',''),'%Y%m%d%H%M%S')
					db_sp.append(end_time)
				elif (sp[0].strip() == 'Test_time'):db_sp.append(sp[1].strip())				
				elif (sp[0].strip() == 'Operator'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Machine'):
					machine=sp[1].strip()
					db_sp.append(machine)

				elif (sp[0].strip() == 'IP_ADDRESS'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Mac_Address'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Fixture_ID'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Program_ID'):db_sp.append(sp[1].strip())				
				elif (sp[0].strip() == 'Retest'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Average_vacuum'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'MIN_vacuum'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'MAX_vacuum'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Tester_TEMP'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'ESD_IMPEDANCE'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'ESD_VOLTAGE'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Deviation1'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Deviation2'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Deviation3'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Deviation4'):db_sp.append(sp[1].strip())
				elif (sp[0].strip() == 'Deviation5'):
					db_sp.append(sp[1].strip())
					print(db_sp)
	
			line = fp.readline()
		fp.close()
		return {'result': 'Success'}
	"""
	数据接口
	"""
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('file', required=True, type=FileStorage, location='files')

	def post(self,filename):
		result = {"result":"Fail"}
		WriteDbResult = False
		
		try:
			path=os.path.abspath("..")+"newlog/"
			fp = open(path+filename, 'r')
			line = fp.readline()
			db_sp=[]
			board=''
			machine=''
			sn=''
			end_time=''

			while line :
				line = line.strip('{\n}')
				sp=line.split(":")
				if (len(sp)==0 or ("=" in sp[0])): break			
				else :
					if (sp[0].strip() == 'Board'):
						board=sp[1].split()[0].strip()
						db_sp.append(board)
					elif (sp[0].strip() == 'Serial_Number'):
						sn=sp[1].strip()
						db_sp.append(sn)
					elif (sp[0].strip() == 'ICT_STATION'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Cell_No'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Status'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Fail_code'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Start_time'):
						strtime=(sp[1]+sp[2]+sp[3]).strip().replace(' ','')
						start_time=dt.strptime(strtime.replace('-',''),'%Y%m%d%H%M%S')		
						db_sp.append(start_time)
					elif (sp[0].strip() == 'End_time'):
						strtime=(sp[1]+sp[2]+sp[3]).strip().replace(' ','')
						end_time=dt.strptime(strtime.replace('-',''),'%Y%m%d%H%M%S')						
						db_sp.append(end_time)
					elif (sp[0].strip() == 'Test_time'):db_sp.append(sp[1].strip())				
					elif (sp[0].strip() == 'Operator'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Machine'):
						machine=sp[1].strip()
						db_sp.append(machine)

					elif (sp[0].strip() == 'IP_ADDRESS'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Mac_Address'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Fixture_ID'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Program_ID'):db_sp.append(sp[1].strip())				
					elif (sp[0].strip() == 'Retest'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Average_vacuum'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'MIN_vacuum'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'MAX_vacuum'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Tester_TEMP'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'ESD_IMPEDANCE'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'ESD_VOLTAGE'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Deviation1'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Deviation2'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Deviation3'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Deviation4'):db_sp.append(sp[1].strip())
					elif (sp[0].strip() == 'Deviation5'):
						db_sp.append(sp[1].strip())
						if(self.CheckRepeat(board,machine,sn,end_time)):return({"result":filename+" is duplicated"})
						WriteDbResult=self.WriteToDb(db_sp)

		
				line = fp.readline()
			fp.close()

		except Exception as err:
			print("[error]: {0}".format(err))
		
		if WriteDbResult :
			shutil.move(path+filename,os.path.abspath("..")+"processednewlog/")
			result['result'] = 'Success'
		return result

	def CheckRepeat(self,board,machine,sn,end_time):
		conn = mysql2.connect()
		cursor = conn.cursor()
		cursor.execute("select count(*) from ict_detail_result where board='"+board+"' and machine='"+machine+"' and sn='"+sn+"' and end_time='"+str(end_time)+"'")
		result=cursor.fetchall()
		return (result[0]['count(*)']>0)

	def WriteToDb(self,lists):
		#type 0:  log檔基本資訊
		
		Items = 'insert ignore into ict_detail_result(board,sn,ict_station,cell_no,status,fail_code,start_time,end_time,total_time,operator,machine,machine_ip,machine_mac,fixture_id,program_id,retest,avg_vacuum,min_vacuum,max_vacuum,tester_temp,esd_impedance,esd_voltage,deviation1,deviation2,deviation3,deviation4,deviation5) values ('
		
		
		for item in lists:
			if str(item)=="None":Items=Items+'null'+','
			else : Items = Items + '"' + str(item) + '"' + ','
		Items = Items.strip(',')
		Items += ')'
		print (Items)
		try :
			conn = mysql2.connect()
			cursor = conn.cursor()
			cursor.execute(Items)
			conn.commit()
			cursor.close()
			conn.close()
			return True	
		except Exception as inst:
			print('ICT Test Data MySql Write Err:'+Items)
			print(str(inst))
			logging.getLogger('error_Logger').error('ICT Test Data MySql Write Err:'+Items)
			logging.getLogger('error_Logger').error(inst)
			with codecs.open('./Log/ErrPost/newlog_batch_{0}.sql'.format(dt.now().strftime('%Y%m%d')),'ab', "utf-8") as ErrOut :
				ErrOut.write(Items)
				ErrOut.write('\n')
				ErrOut.close()
		return False


		
api.add_resource(NewlogBatch, '/newlog_batch/')


if __name__ == '__main__':
	app.run(debug=True)