#!flask/bin/python

import os
import sys
import datetime

from flask import Flask, jsonify, abort
from flask import render_template, request, url_for

app = Flask(__name__)

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('localhost', 27017)

mongo = client.cloudly


@app.route('/test/', methods = ['GET'])
def test():
	return jsonify( { 'test': True } )


@app.route('/v10/activity/', methods = ['POST'])
def activity():

	data = request.json
	
	activity_log = {
		'secret': data['secret'],
		'uuid': data['uuid'],
		'agent_version': data['agent_version'],
		'activity': data['activity'],
		'date_created': datetime.datetime.now(),
	}
	activity_ = mongo.activity
	activity_.insert( activity_log )

	return jsonify( { 'test': True } )


@app.route('/v10/onboot/', methods = ['GET', 'POST'])
def onboot_vms():
	# XXX onboot_vms
	return jsonify( { 'test': True } )


@app.route('/v10/ping/', methods=['POST'])
def ping():
	
	data = request.json

	if not request.headers.getlist("X-Forwarded-For"):
		ip_remote = request.remote_addr
	else:
		ip_remote = request.headers.getlist("X-Forwarded-For")[0]

	uuid = data['uuid']
	ip = data['ip']
	# XXX
	ip_remote = ip_remote
	secret = data['secret']
	loadavg = data['loadavg']
	uptime = data['uptime']
	cpu_usage = data['cpu_usage']
	cpu_info = data['cpu_info']
	cpu_virtualization = data['cpu_virtualization']
	memory_usage = data['memory_usage']
	physical_disks = data['physical_disks']
	disks_usage = data['disks_usage']
	agent_version = data['agent_version']
	last_seen = datetime.datetime.now()

	server = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'ip': ip,
		'ip_remote': ip_remote,
		'loadavg': loadavg,
		'uptime': uptime,
		'cpu_usage': cpu_usage,
		'cpu_info': cpu_info,
		'cpu_virtualization': cpu_virtualization,
		'memory_usage': memory_usage,
		'physical_disks': physical_disks,
		'disks_usage': disks_usage,
		'last_seen': last_seen,
	}

	print 'Agent-V'+str(agent_version), uuid, secret, 'IP', ip_remote+'/'+ ip, '('+uptime+')'
	print server
	import random
	print '.'*random.randint(10,80)
	
	servers = mongo.servers
	server_ = servers.find_one({'secret':secret, 'uuid':uuid,})

	if(server_): 
		server_ = servers.update({'secret':secret, 'uuid':uuid}, server)
	else:
		servers.insert(server)

	
	loadavg_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'loadavg': loadavg,
		'date_created': datetime.datetime.now(),
	}
	loadavg_ = mongo.loadavg
	loadavg_.insert( loadavg_metrics )

	cpu_usage_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'cpu_usage': cpu_usage,
		'date_created': datetime.datetime.now(),
	}
	cpu_usage_ = mongo.cpu_usage
	cpu_usage_.insert( cpu_usage_metrics )

	memory_usage_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'memory_usage': memory_usage,
		'date_created': datetime.datetime.now(),
	}
	memory_usage_ = mongo.memory_usage
	memory_usage_.insert( memory_usage_metrics )

	disks_usage_metrics = {
		'secret': secret,
		'agent_version': agent_version,
		'uuid': uuid,
		'disks_usage': disks_usage,
		'date_created': datetime.datetime.now(),
	}
	disks_usage_ = mongo.disks_usage
	disks_usage_.insert( disks_usage_metrics )
	

	command_ = {}
	command = mongo.commands.find_one({'secret':secret, 'uuid':uuid,'is_new':True,})

	if(command):

		command_ = { 
			'uuid': command['uuid'], 
			'command': command['command'], 
			'name': command['name'],
			'disk_size': command['disk_size'], 
			'package_link': command['package_link'], 
			'vcpu': command['vcpu'], 
			'ram': command['ram'], 
			'package': command['package'], 
		}
		mongo.commands.update( command, {"is_new":False,} )

		
	return jsonify( { 'thanks': True, 'command': command_, } ), 201




if __name__ == '__main__':
	app.run(
		debug = True,
		host = "0.0.0.0",
		port = 5000
	)
