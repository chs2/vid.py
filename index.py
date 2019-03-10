#!/usr/bin/env python

import cgi
import cgitb
import json
import os
import sys

import controller
import repository

cgitb.enable()


response = {"code": 400, "message": "Bad Request"}

try:
	request = os.environ['PATH_INFO'].strip('/').split('/')
	objectType = request[0][0].upper() + request[0][1:]
	actionName = os.environ['REQUEST_METHOD'].lower()

	controller = getattr(controller, objectType)()
	controller.setRepository(getattr(repository, objectType)())

	response = getattr(controller, actionName)(request)
except:
	response["code"] = 500
	response["message"] = "Internal Server Error"
	
print "Status: {} {}".format(response["code"], response["message"])
print "Content-Type: application/json"
print ""
print json.dumps(response)

