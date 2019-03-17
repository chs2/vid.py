#!/usr/bin/env python

import cgi
import cgitb
import traceback
import json
import os
import sqlite3
import sys

import controller
import exception
import repository

cgitb.enable()

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

response = {"code": 400, "message": "Bad Request"}

try:
	if "HTTP_ACCEPT" not in os.environ:
		raise exception.Http400

	if "application/json" not in os.environ['HTTP_ACCEPT'] and "*/*" not in os.environ['HTTP_ACCEPT']:
		raise exception.Http406

	if "PATH_INFO" not in os.environ:
		raise exception.Http400

	request = os.environ['PATH_INFO'].strip('/').split('/')

	if len(request) == 0 or len(request[0]) == 0:
		raise exception.Http400

	objectType = request[0][0].upper() + request[0][1:]
	actionName = os.environ['REQUEST_METHOD'].lower()

	if not hasattr(controller, objectType):
		raise exception.Http400

	controller = getattr(controller, objectType)()

	if not hasattr(controller, actionName):
		raise exception.Http405

	conn = sqlite3.connect('data/vid-pl.db')
	conn.row_factory = dict_factory
	controller.setRepository(getattr(repository, objectType)(conn))

	response = getattr(controller, actionName)(request)

	conn.close()
except exception.Http as e:
	response["code"] = e.code
	response["message"] = e.message
except BaseException as e:
	response["code"] = 500
	response["message"] = "Internal Server Error"
	response["strerror"] = repr(e)
	response["trace"] = traceback.format_exc()
	
print "Status: {} {}".format(response["code"], response["message"])
print "Content-Type: application/json"
print ""

print json.dumps(response)

