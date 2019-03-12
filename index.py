#!/usr/bin/env python

import cgi
import cgitb
import json
import os
import sqlite3
import sys

import controller
import repository

cgitb.enable()

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

response = {"code": 400, "message": "Bad Request"}

try:
	request = os.environ['PATH_INFO'].strip('/').split('/')
	objectType = request[0][0].upper() + request[0][1:]
	actionName = os.environ['REQUEST_METHOD'].lower()

	controller = getattr(controller, objectType)()
	conn = sqlite3.connect('data/vid-pl.db')
	conn.row_factory = dict_factory
	controller.setRepository(getattr(repository, objectType)(conn))

	response = getattr(controller, actionName)(request)
except Exception as e:
	response["code"] = 500
	response["message"] = "Internal Server Error"
	response["data"] = str(e)
	
print "Status: {} {}".format(response["code"], response["message"])
print "Content-Type: application/json"
print ""

print json.dumps(response)

