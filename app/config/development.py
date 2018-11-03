#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime


# database connection data
DB_CONNECTION = {
	"MONGODB_DB": "HR"
	,"MONGODB_HOST": "192.168.2.201"
	,"MYSQL_DATABASE_HOST":"10.132.46.138"
	,"MYSQL_DATABASE_USER":"root"
	,"MYSQL_DATABASE_PASSWORD":"Foxconn88"
	,"MYSQL_DATABASE_DB":"ICT_Project"
#	,"MYSQL_DATABASE_CHARSET":"utf-8"
	,"MONGO_HOST":"192.168.2.201"
	,"MONGO_DBNAME":"HR"
	,"MYSQL_HOST":"10.132.46.138"
	,"MYSQL_USER":"root"
	,"MYSQL_PASSWORD":"Foxconn88"
	,"MYSQL_DB":"ICT_Project"
}
# Kafka connection data
Kafka_CONNECTION = {
	"Kafka_HOST" :['broker-0.kafka.mesos:54957','broker-1.kafka.mesos:46290','broker-2.kafka.mesos:35873']
	,"Kafka_TryCount":5
}
# Upload File Dir
Upload_Dir = {
	"Flnet_WeekReportDir":"T:/Upload/"
}

# flask vars
FLASK_VARS = {
	'DEBUG': True,
	'SECRET_KEY': 'aReallySecretKey',
}

# another third party libs...
PASSLIB = {
	'HASH_ALGORITHM': 'SHA512',
	'HASH_SALT': 'HiMyNameIsGoku',
}
DEBUG_TB_PANELS = (
	'flask_debugtoolbar.panels.versions.VersionDebugPanel',
	'flask_debugtoolbar.panels.timer.TimerDebugPanel',
	'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
	'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
	'flask_debugtoolbar.panels.template.TemplateDebugPanel',
	'flask_debugtoolbar.panels.logger.LoggingPanel',
	'flask_mongoengine.panels.MongoDebugPanel'
)

DEBUG_TB_INTERCEPT_REDIRECTS = False
