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

@restapi.resource('/wirelist/<string:filename>')
class Wirelist(Resource):
	def get(self,filename):
		path=os.path.abspath("..")+"wirelist/"

		fp = open(path+filename, 'r')

		line = fp.readline()
		board = filename

		while line :
			sp=line.replace('"','').split()

			if (len(sp)==0 or sp[0] == 'end'): line = fp.readline() 
			else :
				if (sp[0] == 'test'):
					#if (sp[1]=='analog') :
					test_type=sp[1]
					if (sp[1]=='powered' and sp[2]=='shorts'):
						test_type=sp[1]+' '+sp[2]
						#component=sp[3]
					if(sp[2]!='.discharge'):
						component=sp[len(sp)-1]
						subtest=''
						line=fp.readline()
						while line:
							sp = line.replace('"','').split()
							if (len(sp)>0):
								if(sp[0]=='subtest'):
									subtest=sp[1]

								elif (sp[0]=='wire'):
									db_sp=(board,test_type,component,subtest,sp[1],sp[3],sp[4])
									print(db_sp)
								
								elif(sp[0]=='end' and sp[1]=='test'):break

							line=fp.readline()
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
			path=os.path.abspath("..")+"wirelist/"

			fp = open(path+filename, 'r')

			line = fp.readline()
			board = filename

			while line :
				line.replace('"','')
				sp=line.replace('"','').split()

				if (len(sp)==0 or sp[0] == 'end'): line = fp.readline() 
				else :
					if (sp[0] == 'test'):

						test_type=sp[1]
						if (sp[1]=='powered' and sp[2]=='shorts'):
							test_type=sp[1]+' '+sp[2]
						
						if(sp[2]!='.discharge'):
							component=sp[len(sp)-1]
							subtest=''
							line=fp.readline()
							while line:
								sp = line.replace('"','').split()
								if (len(sp)>0):
									if(sp[0]=='subtest'):
										subtest=sp[1]

									elif(sp[0]=='device'):
										component=(sp[1].split(';'))[0]

									elif (sp[0]=='wire'):
										db_sp=(board,test_type,component,subtest,sp[1],sp[3],sp[4])
										WriteDbResult = self.WriteToDb(db_sp,0)
									
									elif(sp[0]=='end' and sp[1]=='test'):break
									
								line=fp.readline()
						line=fp.readline()
	
				line = fp.readline()
			fp.close()

		except Exception as err:
			print("[error]: {0}".format(err))
		
		if WriteDbResult :
			result['result'] = 'Success'
		return result

	def WriteToDb(self,lists,type):
		if (type == 0) :
			Items = 'insert ignore into ICT_Project.wirelist(board,test_type,component,subtest,node,BRC,mark) values ('
		
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
			with codecs.open('./Log/ErrPost/wirelist_{0}.sql'.format(dt.now().strftime('%Y%m%d')),'ab', "utf-8") as ErrOut :
				ErrOut.write(Items)
				ErrOut.write('\n')
				ErrOut.close()
		return False


		
api.add_resource(Wirelist, '/wirelist/')


if __name__ == '__main__':
	app.run(debug=True)