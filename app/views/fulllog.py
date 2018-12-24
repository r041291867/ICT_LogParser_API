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
from app.utils import cache_key

app = Flask(__name__)
api = Api(app=app)

@restapi.resource('/fulllog')
# @restapi.resource('/Data')
class DataApi(Resource):

	def get(self):
		file = request.files['file']
		filename=file.filename

		# check if file exist 
		if(filename==''):return({"result":"No file."})
		# check file type
		if(filename.rsplit('.',1)[1].lower()!='txt'):return({"result":"File type should be txt."})

		# set file path
		path=os.path.abspath("..")+"fulllog/"
		# save file 
		file.save(os.path.join(path,filename))
		# open file
		fp = open(path+filename, "r")

		line = fp.readline()
		machine = ''
		sn_code = ''		
		EndTime = ''
		board = ''
		isAnalogPowered=False
		while line :
			if (line == '}\n' or line == '}}'): line = fp.readline()
			else :
				line = line.strip('{@\n}')
				sp = line.split("|")
				db_sp = [] 	
				
				while '' in sp: sp.remove('')
				#處理要寫入ict_result資料
				if (len(sp)>0 and sp[0] == 'BATCH') :
					db_sp.append(sp[1])
					db_sp.append(sp[7])
					db_sp.append(sp[8])
					logtime = sp[6]
					machine = sp[8]
					board = sp[1]
					line = fp.readline()
					sp = line.split("|")
			
					while '' in sp: sp.remove('')
					sn_code = sp[1]
					db_sp.append(sp[1])
					db_sp.append(sp[2])
					
					#日期格式轉換
					Btime = dt.strptime('20'+sp[3], '%Y%m%d%H%M%S')     #BeginTime
					Etime = dt.strptime('20'+sp[9], '%Y%m%d%H%M%S')		#EndTime
					Ltime = dt.strptime('20'+logtime, '%Y%m%d%H%M%S')   #LogTime
					EndTime = Etime
					
					db_sp.append(Btime)
					db_sp.append(Etime)
					db_sp.append(Ltime)
					print (db_sp)

				#處理各測試結果資料(pre-short、open/short、testjet、analog、poweron、digital、boundary scan、analog powered、frequency、programming)
				elif (len(sp)>0 and sp[0] == 'BLOCK') :
					db_sp.append(sp[1])
					db_sp.append(sp[2])
					# 若sp第一個元素為pwr_check、pwr_check_pro、pwr_check_iso則為power_on_result
					if(db_sp[0]=='pwr_check' or db_sp[0]=='pwr_check_pro' or db_sp[0]=='pwr_check_iso') : isPowerOn=True
					else : isPowerOn=False 
					line = fp.readline()
					while line :		#block內可能有好幾個不同的測試

						if (line == '}\n'): 
							if (db_sp[0] == 'pwr_check'):     #若讀到pwr_check結尾}代表接下來遇到的A-MEA皆屬於AnalogPowered測試結果
								isAnalogPowered=True     
								isPowerOn=False
							break
							
						else :
							line = line.strip('{@\n}') #移除頭尾@\n
							sp = line.split("{@")
							while '' in sp: sp.remove('')
							lines = []
							for item in sp:
								line = line.strip('{@\n}')
								lines += item.split("|")
							db_sp_new = db_sp + lines
							db_sp_new.insert(0,machine)
							db_sp_new.insert(1,sn_code)
							db_sp_new.append(EndTime)

							if (db_sp_new[4] == 'A-JUM') :
								del db_sp_new[3]		#刪除不必要元素
								del db_sp_new[3]
								print (db_sp_new)

							elif (db_sp_new[4] == 'TS'):
								del db_sp_new[3]		#刪除不必要元素
								del db_sp_new[3]
								print (db_sp_new)

							elif (db_sp_new[4] == 'A-CAP' or db_sp_new[4] == 'A-RES' or db_sp_new[4] == 'A-MEA' \
							 or db_sp_new[4] == 'A-DIO' or db_sp_new[4] == 'A-NFE' or db_sp_new[4] == 'A-PFE' \
							 or db_sp_new[4] == 'A-NPN' or db_sp_new[4] == 'A-PNP' or db_sp_new[4] == 'A-ZEN'):
								
								if (db_sp_new[7]=='LIM2'): db_sp_new.insert(8,None)
								if (db_sp_new[8]=='LIM2') : db_sp_new.insert(9,None) #沒有nominal,需補空值							
								if (len(db_sp_new)<13) : db_sp_new.insert(7,'') #沒有test_condition
								if(isPowerOn and db_sp_new[4] == 'A-MEA'):
									del db_sp_new[4] #analog powered不需要test_type
								elif(isAnalogPowered and db_sp_new[4] == 'A-MEA'):
									del db_sp_new[4] #PowerOn不需要component、test_type
								print (db_sp_new)
							line = fp.readline()
				
				elif (len(sp)>0 and sp[0] == 'TJET'):
					db_sp_new = [machine,sn_code,sp[1],sp[3],EndTime,board]
					print (db_sp_new)

					# testjet fail RPT parsing
					if(db_sp_new[2]=='01'):
						line=fp.readline()
						while line:
					
							if (line == '}\n' or line.split("|")[0]=='{@DPIN'):break
							else:
								#移除頭尾@\n
								line = line.strip('{@\n}') 
								# split |
								sp = line.split("|")
								db_sp = []
								db_sp = sp[1].split()
								if(sp[0]=='RPT' and len(db_sp)>0) :

									if(db_sp[0]=='Open'):
										#取得第二個元素並移除#字號後取得fail_no
										db_sp_new.append(db_sp[1].replace('#',''))
									elif(db_sp[0]=='Pin' and len(db_sp_new)<8):
										db_sp_new.append(db_sp[1])
										db_sp_new.append(db_sp[3])
									elif(db_sp[0]=='Measured'):
										db_sp_new.append(db_sp[1])
										db_sp_new.append(db_sp[3])
										print(db_sp_new)
										del db_sp_new[6:11]
										
									elif('--' in db_sp[0]):break
									
									line=fp.readline()
						
				elif (len(sp)>0 and sp[0] == 'PF'):
					line = line.strip('{@\n}') 
					sp = line.split("|") 
					db_sp_new=[machine,sn_code,EndTime,sp[2]]
					test_time=''
					if (sp[2]=='0'):
						# 若pass無BRC和fail時間
						db_sp_new.append(None)
						db_sp_new.append(None)
						print(db_sp_new)
					else:	
						line=fp.readline()						
						while line:	
							line = line.strip('{@\n}') 
							print(line)
							sp = line.split("|") 							
							db_sp=sp[1].split()
							if (sp[0]=='RPT' and db_sp[0]=='CHEK-POINT'):
								line=fp.readline()
								line = line.strip('{@\n}')  
								str_test_time=(line.split('|'))[1].replace('}','')
								test_time=dt.strptime(str_test_time,'%a %b %d %H:%M:%S %Y')
							elif (sp[0]=='RPT' and '(' in db_sp[0]):
								db_sp_new.append(test_time)
								db_sp_new.append(db_sp[0].replace('(','').replace(')',''))
								print(db_sp_new)
								# 處理多筆PF測試fail log
								del db_sp_new[4:7]
							elif ('End' in sp[1] or 'PIN' in sp[0]):
								break

							line=fp.readline()

				elif (len(sp)>0 and sp[0] == 'TS') :
					db_sp_new = [machine,sn_code,sp[1],sp[5],EndTime]
					print (db_sp_new)

					#若測試狀態為失敗,需parsing fail report
					if (sp[1]=='1'):
						line=fp.readline()
						test_time=''

						while line:

							if (line == '}\n'): break
				
							else:
								#移除頭尾@\n
								line = line.strip('{@\n}') 

								#split |
								sp = line.split("|")
								db_sp = [] 
								db_sp = sp[1].split()
																
								#陣列第一個元素為RPT且第二個元素用空白切割後陣列長度大於0
								if (sp[0]=='RPT' and len(db_sp)>0):
									
									# 取得fail 時間
									if(db_sp[0]=='Shorts'):
										line=fp.readline().strip('{@\n}')
										str_test_time=(line.split('|'))[1].replace('}','')
										test_time=dt.strptime(str_test_time,'%a %b %d %H:%M:%S %Y')
								
									#陣列第一個元素為Short或Open
									elif (db_sp[0]=='Short' or db_sp[0]=='Open'):
										db_sp_new = [machine,sn_code,EndTime,test_time]
										#取得第fail_type為Short/Open
										db_sp_new.append(db_sp[0])
										#取得第二個元素並移除#字號後取得fail_no
										db_sp_new.append(db_sp[1].replace('#',''))
						 		
									#From為fail point起點 To為fail point終點
									elif(db_sp[0]=='From:' or db_sp[0]=='To:'):
										#若遇到針點為v需取下一行才是針點名稱
										if(db_sp[1]=='v'):
											line=fp.readline()
											point = (line.split())[0].split("|")
											db_sp_new.append(point[1])
										else :
											db_sp_new.append(db_sp[1])
										db_sp_new.append(db_sp[2])

										# ohms
										if(len(db_sp)>3 and db_sp[3]!='Open'):
											db_sp_new.append(db_sp[3])
										else:db_sp_new.append(None)
												
									#讀到Common視為其中一項fail結束
									elif (db_sp[0]=='Common'):print(db_sp_new)
										
									#fail Report結束
									elif ('End' in db_sp[0]):break

									line=fp.readline()

								else : line=fp.readline()	        
				
				# 上電測試-Digital result
				elif (len(sp)>0 and sp[0] == 'D-T') :
					db_sp_new=[]
					db_sp_new.insert(0,machine)
					db_sp_new.insert(1,sn_code)
					if(sp[1]=='1') : db_sp_new.append(sp[5])
					else : db_sp_new.append(sp[4])
					db_sp_new.append(sp[1])
					db_sp_new.append(EndTime)
					print (db_sp_new)
					
				# 上電測試-BoundaryScan result
				elif (len(sp)>0 and sp[0] == 'BS-CON') :
					db_sp_new=[]
					db_sp_new.insert(0,machine)
					db_sp_new.insert(1,sn_code)
					db_sp_new.append(sp[1])
					db_sp_new.append(sp[2])
					db_sp_new.append(EndTime)
					print (db_sp_new)


				line = fp.readline()
		fp.close()
		return {'result': 'Success'}
	"""
	数据接口
	"""
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('file', required=True, type=FileStorage, location='files')

	def post(self):
		file = request.files['file']
		filename=file.filename

		# check if file exist 
		if(filename==''):return({"result":"No file."})
		# check file type
		if(filename.rsplit('.',1)[1].lower()!='txt'):return({"result":"File type should be txt."})

		# set file path
		path=os.path.abspath("..")+"fulllog/"
		# save file 
		file.save(os.path.join(path,filename))
		
		result = {"result":"Fail"}
		WriteDbResult = False
		insert_list=[]  #insert sql list

		try:
			fp = open(path+filename, "r")
			line = fp.readline()
			machine = ''
			sn_code = ''        
			EndTime = ''
			board = ''
			isAnalogPowered=False
			while line :
				if (line == '}\n' or line == '}}'): line = fp.readline()	#遇到'}'不處理
				else :
					line = line.strip('{@\n}') #去除外圍的括號與＠
					sp = line.split("|")
					db_sp = [] 
					
					#去除空字串
					while '' in sp: sp.remove('')
					if (len(sp)>0 and sp[0] == 'BATCH') :
						db_sp.append(sp[1])
						db_sp.append(sp[7])
						db_sp.append(sp[8])
						logtime = sp[6]
						machine = sp[8]
						board = sp[1]
						line = fp.readline()
						sp = line.split("|")
						while '' in sp: sp.remove('')
						sn_code = sp[1]
						db_sp.append(sp[1])
						db_sp.append(sp[2])
						#日期格式轉換
						Btime = dt.strptime('20'+sp[3], '%Y%m%d%H%M%S')     #BeginTime
						Etime = dt.strptime('20'+sp[9], '%Y%m%d%H%M%S')		#EndTime
						Ltime = dt.strptime('20'+logtime, '%Y%m%d%H%M%S')   #LogTime
						EndTime = Etime
		
						# check if file is repeat
						if(self.CheckRepeat(machine,sn_code,Etime)):return({"result":filename+" is duplicated"})

						db_sp.append(Btime)
						db_sp.append(Etime)
						db_sp.append(Ltime)
						insert_list.append(self.CombineSqlStr(db_sp,0))

					elif (len(sp)>0 and sp[0] == 'BLOCK') :
						db_sp.append(sp[1])
						db_sp.append(sp[2])
						# 若sp第一個元素包含(pwr_check)字串則該block區塊內的A-MEA為power_on_result
						if(db_sp[0]=='pwr_check' or db_sp[0]=='pwr_check_pro' or db_sp[0]=='pwr_check_iso') : isPowerOn=True
						else : isPowerOn=False 		
						line = fp.readline()
						while line :		#block內可能有好幾個不同的測試
							if (line == '}\n'): 
								if (db_sp[0] == 'pwr_check'):     #若讀到pwr_check結尾}則將接下來的A-MEA視為AnalogPoweredResult
									isAnalogPowered=True     
									isPowerOn=False
								break			
								
							else :
								line = line.strip('{@\n}')
								sp = line.split("{@")
								while '' in sp: sp.remove('')
								lines = []
								for item in sp:
									line = line.strip('{@\n}')
									lines += item.split("|")
								db_sp_new = db_sp + lines
								
								db_sp_new.insert(0,machine)
								db_sp_new.insert(1,sn_code)
								db_sp_new.append(EndTime)

								if (db_sp_new[4] == 'A-JUM'):
									del db_sp_new[3]		#刪除不必要元素
									del db_sp_new[3]
									insert_list.append(self.CombineSqlStr(db_sp_new,1))
									
								elif (db_sp_new[4] == 'A-CAP' or db_sp_new[4] == 'A-RES' or db_sp_new[4] == 'A-MEA' \
									or db_sp_new[4] == 'A-DIO' or db_sp_new[4] == 'A-NFE' or db_sp_new[4] == 'A-PFE' \
						 			or db_sp_new[4] == 'A-NPN' or db_sp_new[4] == 'A-PNP' or db_sp_new[4] == 'A-ZEN'):
									
									dbType=4

									if (db_sp_new[7]=='LIM2'): db_sp_new.insert(8,None) #沒有nominal,需補空值	 
									if (db_sp_new[8]=='LIM2') : db_sp_new.insert(9,None) #沒有nominal,需補空值							
									if (len(db_sp_new)<13) : db_sp_new.insert(7,'') #沒有test_condition
									if(isPowerOn and db_sp_new[4] == 'A-MEA'):
										del db_sp_new[4]   #PowerOn不需要component、test_type
										dbType=5
									elif(isAnalogPowered and db_sp_new[4] == 'A-MEA'):
										del db_sp_new[4]     #analog powered不需要test_type
										dbType=8

									if(dbType==4 and board=='73-18275-04'):
										dbType=41
										db_sp_new.append(board)					

									insert_list.append(self.CombineSqlStr(db_sp_new,dbType))
									
								line = fp.readline()

					# 模擬測試-Testjet
					elif (len(sp)>0 and sp[0] == 'TJET'):
						db_sp_new = [machine,sn_code,sp[1],sp[3],EndTime,board]
						
						insert_list.append(self.CombineSqlStr(db_sp_new,3))

						# testjet fail RPT parsing
						if(db_sp_new[2]=='01'):
							line=fp.readline()
							while line:
						
								if (line == '}\n' or line.split("|")[0]=='{@DPIN'):break
								else:
									#移除頭尾@\n
									line = line.strip('{@\n}') 
									# split |
									sp = line.split("|")
									db_sp = []
									db_sp = sp[1].split()
									if(sp[0]=='RPT' and len(db_sp)>0) :

										if(db_sp[0]=='Open'):
											#取得第二個元素並移除#字號後取得fail_no
											db_sp_new.append(db_sp[1].replace('#',''))
										elif(db_sp[0]=='Pin' and len(db_sp_new)<8):
											db_sp_new.append(db_sp[1])

										elif(db_sp[0]=='Measured'):
											db_sp_new.append(db_sp[1])
											insert_list.append(self.CombineSqlStr(db_sp_new,31))
											del db_sp_new[6:9]
										
										elif('--' in db_sp[0]):break
										
										line=fp.readline()

					elif (len(sp)>0 and sp[0] == 'PF'):
						line = line.strip('{@\n}') 
						sp = line.split("|") 
						db_sp_new=[machine,sn_code,EndTime,sp[2]]
						test_time=''
						if (sp[2]=='0'):
							# 若pass無BRC和fail時間
							db_sp_new.append(None)
							db_sp_new.append(None)
							insert_list.append(self.CombineSqlStr(db_sp_new,9))
						else:	
							line=fp.readline()						
							while line:	
								line = line.strip('{@\n}') 
								sp = line.split("|") 
								db_sp=sp[1].split()
								if (sp[0]=='RPT' and db_sp[0]=='CHEK-POINT'):
									line=fp.readline()
									line = line.strip('{@\n}')  
									str_test_time=(line.split('|'))[1].replace('}','')
									test_time=dt.strptime(str_test_time,'%a %b %d %H:%M:%S %Y')
								elif (sp[0]=='RPT' and '(' in db_sp[0]):
									db_sp_new.append(test_time)
									db_sp_new.append(db_sp[0].replace('(','').replace(')',''))
									insert_list.append(self.CombineSqlStr(db_sp_new,9))
									del db_sp_new[4:7]
								elif ('End' in sp[1] or 'PIN' in sp[0]):
									break

								line=fp.readline()	

					# 模擬測試-open_short
					elif (len(sp)>0 and sp[0] == 'TS') :
						db_sp_new = [machine,sn_code,sp[1],EndTime]
						insert_list.append(self.CombineSqlStr(db_sp_new,2))
						#若測試狀態為失敗,需parsing fail report
						if (sp[1]=='1'):
							line=fp.readline()
							test_time=''
							while line:
								if (line == '}\n'): break #遇到'}'不處理
				
								else:
									#移除頭尾@\n split |
									line = line.strip('{@\n}') 
									sp = line.split("|") 									
									db_sp = [] 
									db_sp = sp[1].split()

									#陣列第一個元素為RPT且第二個元素用空白切割後陣列長度大於0
									if (sp[0]=='RPT' and len(db_sp)>0):

										# 取得fail 時間
										if(db_sp[0]=='Shorts'):
											
											line=fp.readline().strip('{@\n}')
											str_test_time=(line.split('|'))[1].replace('}','')
											test_time=dt.strptime(str_test_time,'%a %b %d %H:%M:%S %Y')
										
										#陣列第一個元素為Short或Open
										elif (db_sp[0]=='Short' or db_sp[0]=='Open'):
											db_sp_new = [machine,sn_code,EndTime]
											db_sp_new.append(test_time)
											#取得第fail_type為Short/Open
											db_sp_new.append(db_sp[0])
											#取得第二個元素並移除#字號後取得fail_no
											db_sp_new.append(db_sp[1].replace('#',''))

										#From為fail point起點 To為fail point終點
										elif(db_sp[0]=='From:' or db_sp[0]=='To:'):
											#若遇到針點為v需取下一行才是針點名稱
											if(db_sp[1]=="v"):
												line=fp.readline()
												point = (line.split())[0].split("|")
												
												db_sp_new.append(point[1])
											else :
												db_sp_new.append(db_sp[1])
											db_sp_new.append(db_sp[2])

											# ohms
											if(len(db_sp)>3 and db_sp[3]!='Open'):
												db_sp_new.append(db_sp[3])
											else:db_sp_new.append(None)
													
										#讀到Common視為其中一項fail結束
										elif (db_sp[0]=='Common'):

											insert_list.append(self.CombineSqlStr(db_sp_new,21))
											
										#fail Report結束
										elif ('End' in db_sp[0]): break

										line=fp.readline()

									else : line=fp.readline()	        
					
					# 上電測試-Digital result
					elif (len(sp)>0 and sp[0] == 'D-T') :
						db_sp_new=[]
						db_sp_new.insert(0,machine)
						db_sp_new.insert(1,sn_code)
						if(sp[1]=='1') : db_sp_new.append(sp[5])
						else : db_sp_new.append(sp[4])
						db_sp_new.append(sp[1])
						db_sp_new.append(EndTime)
						insert_list.append(self.CombineSqlStr(db_sp_new,6))
					
					# 上電測試-BoundaryScan result
					elif (len(sp)>0 and sp[0] == 'BS-CON') :
						db_sp_new=[]
						db_sp_new.insert(0,machine)
						db_sp_new.insert(1,sn_code)
						db_sp_new.append(sp[1])
						db_sp_new.append(sp[2])
						db_sp_new.append(EndTime)

						insert_list.append(self.CombineSqlStr(db_sp_new,7))
					line = fp.readline()

			fp.close()
			WriteDbResult=self.WriteToDb(insert_list)
			
			

		except Exception as err:
			# print(filename)
			print("[error]: {0}".format(err))
		
		if WriteDbResult :
			#移動處理完的檔案到上一層的processedlog資料夾中
			shutil.move(path+filename,os.path.abspath("..")+"processedlog/")
			result['result'] = 'Success'
		return result

	def CheckRepeat(self,machine,sn,end_time):
		conn = mysql2.connect()
		cursor = conn.cursor()
		cursor.execute("select count(*) from ICT_Project.ict_result where machine='"+machine+"' and sn='"+sn+"' and end_time='"+str(end_time)+"'")
		result=cursor.fetchall()
		return (result[0]['count(*)']>0)

	def CombineSqlStr(self,lists,type):
		#type 0:  log檔基本資訊
		#type 1:  jumper測試
		#type 2:  short測試
		#type 21: short fail RPT
		#type 3:  testjet
		#type 31: testjet fail RPT
		#type 4:  analog
		#type 41: analog_18275
		#type 5:  power on 
		#type 6:  digital
		#type 7:  boundary scan
		#type 8:  analog_powered
		#type 9:  PF test
		if (type == 0) :
			Items = 'insert ignore into ICT_Project.ict_result(board,operator,machine,sn,status,start_time,end_time,log_time) values ('
		elif (type == 1) :
			Items = 'insert ignore into ICT_Project.preshort_result(machine,sn,component,status,measured,limit_type,high_limit,low_limit,end_time) values ('
		elif (type == 2) :
			Items = 'insert ignore into ICT_Project.open_short_result(machine,sn,status,end_time) values ('
		elif (type == 21) :
			Items = 'insert ignore into ICT_Project.open_short_fail(machine,sn,end_time,fail_time,fail_type,fail_no,from_point,from_BRC,from_ohms,end_point,end_BRC,end_ohms) values ('
		elif (type == 3) :
			Items = 'insert ignore into ICT_Project.testjet_result(machine,sn,status,device,end_time,board) values ('
		elif (type == 31) :
			Items = 'insert ignore into ICT_Project.testjet_fail(machine,sn,status,device,end_time,board,fail_no,pins,node,measured,BRC) values ('		
		elif (type == 4) :
			Items = 'insert ignore into ICT_Project.analog_result(machine,sn,component,block_status,test_type,status,measured,test_condition,limit_type,nominal,high_limit,low_limit,end_time) values ('
		elif (type == 41):
			Items = 'insert ignore into ICT_Project_V2.analog_result_18275(machine,sn,component,block_status,test_type,status,measured,test_condition,limit_type,nominal,high_limit,low_limit,end_time,board) values ('		
		elif (type == 5) :
			Items = 'insert ignore into ICT_Project.power_on_result(machine,sn,power_check_type,block_status,status,measured,power_check,limit_type,nominal,high_limit,low_limit,end_time) values ('				
		elif (type == 6) :
			Items = 'insert ignore into ICT_Project.digital_result(machine,sn,component,status,end_time) values ('
		elif (type == 7) :
			Items = 'insert ignore into ICT_Project.boundary_scan_result(machine,sn,component,status,end_time) values ('
		elif (type == 8) :
			Items = 'insert ignore into ICT_Project.analog_powered_result(machine,sn,component,block_status,status,measured,test_condition,limit_type,nominal,high_limit,low_limit,end_time) values ('
		elif (type == 9) :
			Items = 'insert ignore into ICT_Project.pins_check_result(machine,sn,end_time,status,fail_time,BRC) values ('
			
		
		for item in lists:
			if str(item)=="None":Items=Items+'null'+','
			else : Items = Items + '"' + str(item) + '"' + ','
		Items = Items.strip(',')
		Items += ')'
		return(Items)

	def WriteToDb(self,insert_list):
		try :
			print(insert_list)
			conn = mysql2.connect()
			cursor = conn.cursor()

			for item in insert_list:
				cursor.execute(item)

			conn.commit()
			cursor.close()
			conn.close()
			return True	
		except Exception as inst:
			print('ICT Data MySql Write Err:'+item)
			print(str(inst))
			logging.getLogger('error_Logger').error('ICT Data MySql Write Err:'+item)
			logging.getLogger('error_Logger').error(inst)
			with codecs.open('./Log/ErrPost/Test_{0}.sql'.format(dt.now().strftime('%Y%m%d%H%M%S')),'wb', "utf-8") as ErrOut :
				ErrOut.write(item)
				ErrOut.write('\n')
				ErrOut.close()
			try:
				conn.rollback()
			except: pass
		return False
		
api.add_resource(DataApi, '/fulllog/')


if __name__ == '__main__':
	app.run(debug=True)