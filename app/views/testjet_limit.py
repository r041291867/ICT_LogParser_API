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

@restapi.resource('/testjet_limit/<string:filename>')
class Testjet(Resource):
	def get(self,filename):
		path=os.path.abspath("..")+"testjet_limit/"

		fp = open(path+filename, 'r')

		line = fp.readline()
		board = filename

		while line :
			sp=line.replace('"','').split()

			if (len(sp)>0 and sp[0] == 'device'):
				# print(line)
				device=sp[1]
				low_limit=''
				high_limit=''
				db_sp=[]
				db_sp.append(board)
				db_sp.append(device)
				line=fp.readline()
				while line:
					# print(line)
					sp = line.replace(';',' ').replace(',','').split()
					
					if (len(sp)>0):
						if(sp[0]=='end'):break
						elif(len(sp)>1 and sp[0]=='test' and sp[1]=='pins'):
							low_limit=sp[5]
							high_limit=sp[7]
							db_sp.append(sp[2])
							db_sp.append(low_limit)
							db_sp.append(high_limit)
							if(db_sp[3]!='' and db_sp[4]!=''):print(db_sp)
							
							del db_sp[2:5]

						elif(sp[0]=='pins'):
							db_sp.append(sp[1])
							db_sp.append(low_limit)
							db_sp.append(high_limit)
							if(db_sp[3]!='' and db_sp[4]!=''):print(db_sp)
							del db_sp[2:5]

						elif(sp[0]=='inaccessible'):
							del sp[0]
							del sp[0]
							for x in range(len(sp)):
								db_sp.append(sp[x])
								db_sp.append(low_limit)
								db_sp.append(high_limit)
								if(db_sp[3]!='' and db_sp[4]!=''):print(db_sp)
								del db_sp[2:5]

						line=fp.readline()
	
			line = fp.readline()
		fp.close()
		return {'hello': 'world'}
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
			path=os.path.abspath("..")+"testjet_limit/"
			# filename='73-18275-04'
			fp = open(path+filename, 'r')

			line = fp.readline()
			board = filename

			while line :
				sp=line.replace('"','').split()

				if (len(sp)>0 and sp[0] == 'device'):
					# print(line)
					device=sp[1]
					low_limit=''
					high_limit=''
					db_sp=[]
					db_sp.append(board)
					db_sp.append(device)
					line=fp.readline()
					while line:
						# print(line)
						sp = line.replace(';',' ').replace(',','').split()
						
						if (len(sp)>0):
							if(sp[0]=='end'):break
							elif(len(sp)>1 and sp[0]=='test' and sp[1]=='pins'):
								low_limit=sp[5]
								high_limit=sp[7]
								db_sp.append(sp[2])
								db_sp.append(low_limit)
								db_sp.append(high_limit)
								if(db_sp[3]!='' and db_sp[4]!=''):WriteDbResult=self.WriteToDb(db_sp)
								
								del db_sp[2:5]

							elif(sp[0]=='pins'):
								db_sp.append(sp[1])
								db_sp.append(low_limit)
								db_sp.append(high_limit)
								if(db_sp[3]!='' and db_sp[4]!=''):WriteDbResult-self.WriteToDb(db_sp)
								del db_sp[2:5]

							elif(sp[0]=='inaccessible'):
								del sp[0]
								del sp[0]
								for x in range(len(sp)):
									db_sp.append(sp[x])
									db_sp.append(low_limit)
									db_sp.append(high_limit)
									if(db_sp[3]!='' and db_sp[4]!=''):WriteDbResult=self.WriteToDb(db_sp)
									del db_sp[2:5]

							line=fp.readline()
		
				line = fp.readline()
			fp.close()

		except Exception as err:
			print("[error]: {0}".format(err))
		
		if WriteDbResult :
			result['result'] = 'Success'
		return result

	def WriteToDb(self,lists):
		
		Items = 'insert ignore into ICT_Project.testjet_limit(board,device,pins,low_limit,high_limit) values ('
		
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
			logging.getLogger('error_Logger').error('FulearnV4 Test Data MySql Write Err:'+Items)
			logging.getLogger('error_Logger').error(inst)
			with codecs.open('./Log/ErrPost/testjetlimit_{0}.sql'.format(dt.now().strftime('%Y%m%d')),'ab', "utf-8") as ErrOut :
				ErrOut.write(Items)
				ErrOut.write('\n')
				ErrOut.close()
		return False


		
api.add_resource(Testjet, '/testjet_limit/')


if __name__ == '__main__':
	app.run(debug=True)