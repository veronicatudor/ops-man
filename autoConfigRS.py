import argparse
from pprint import pprint
import json
import ConfigParser

config = ConfigParser.ConfigParser()
try:
    config.read("../hosts")
except Exception as e:
    print 'Something went bad when opening the hosts file', e.value


#retrieve hostnames
options = config.options("ReplicaSet")
hosts = [ "mdb1.demo","mdb2.demo","mdb3.demo" ]

# retrieve relpica set name and the port numbers for the mongod processes
rs_name = config.get("local:vars", "rs_name")
ports = config.get("local:vars", "rs_mongod_ports")
ports = ports.split(" ")

# the configuration file use to create the replica set with Ops Manager
templateDoc = {
   "options": {
        "downloadBase": "/var/lib/mongodb-mms-automation",
        "downloadBaseWindows": "C:\\mongodb-mms-automation"
    },
    "mongoDbVersions": [
        {"name": "3.6.2"}
    ],
    "backupVersions": [],
    "monitoringVersions": [ ],
    "processes": [
        {
            "args2_6": {
                "net": {
                    "port": 28000
                },
                "replication": {
                    "replSetName": "blue"
                },
                "storage": {
                    "dbPath": "/data/blue_0"
                },
                "systemLog": {
                    "destination": "file",
                    "path": "/data/blue_0/mongodb.log"
                }
            },
            "hostname": "MACHINE_HOSTNAME",
            "logRotate": {
                "sizeThresholdMB": 1000,
                "timeThresholdHrs": 24
            },
            "name": "blue_0",
            "processType": "mongod",
            "version": "3.6.2",
            "featureCompatibilityVersion":"3.4",
            "authSchemaVersion": 3
        },
        {
            "args2_6": {
                "net": {
                    "port": 28001
                },
                "replication": {
                    "replSetName": "blue"
                },
                "storage": {
                    "dbPath": "/data/blue_1"
                },
                "systemLog": {
                    "destination": "file",
                    "path": "/data/blue_1/mongodb.log"
                }
            },
            "hostname": "MACHINE_HOSTNAME",
            "logRotate": {
                "sizeThresholdMB": 1000,
                "timeThresholdHrs": 24
            },
            "name": "blue_1",
            "processType": "mongod",
            "version": "3.6.2",
            "featureCompatibilityVersion":"3.4",
            "authSchemaVersion": 3
        },
        {
            "args2_6": {
                "net": {
                    "port": 28002
                },
                "replication": {
                    "replSetName": "blue"
                },
                "storage": {
                    "dbPath": "/data/blue_2"
                },
                "systemLog": {
                    "destination": "file",
                    "path": "/data/blue_2/mongodb.log"
                }
            },
            "hostname": "MACHINE_HOSTNAME",
            "logRotate": {
                "sizeThresholdMB": 1000,
                "timeThresholdHrs": 24
            },
            "name": "blue_2",
            "processType": "mongod",
            "version": "3.6.2",
            "featureCompatibilityVersion":"3.4",
            "authSchemaVersion": 3
        }
    ],
    "replicaSets": [
        {
            "_id": "blue",
            "members": [
                {
                    "_id": 0,
                    "host": "blue_0"
                },
                {
                    "_id": 1,
                    "host": "blue_1"
                },
                {
                    "_id": 2,
                    "host": "blue_2"
                }
            ]
        }
    ],
    "roles": [],
    "sharding": []
}

# name for the processes must be different in case deployed on the same host
templateDoc["processes"][0]["name"] = rs_name + "0_" + ports[0]
templateDoc["processes"][1]["name"] = rs_name + "1_" + ports[1]
templateDoc["processes"][2]["name"] = rs_name + "2_" + ports[2]

templateDoc["processes"][0]["hostname"] = hosts[0]
templateDoc["processes"][1]["hostname"] = hosts[1]
templateDoc["processes"][2]["hostname"] = hosts[2]


templateDoc["processes"][0]["args2_6"]["net"]["port"] = ports[0]
templateDoc["processes"][1]["args2_6"]["net"]["port"] = ports[1]
templateDoc["processes"][2]["args2_6"]["net"]["port"] = ports[2]

templateDoc["processes"][0]["args2_6"]["replication"]["replSetName"] = rs_name
templateDoc["processes"][1]["args2_6"]["replication"]["replSetName"] = rs_name
templateDoc["processes"][2]["args2_6"]["replication"]["replSetName"] = rs_name

templateDoc["replicaSets"][0]["_id"] = rs_name

templateDoc["replicaSets"][0]["members"][0]["host"] = hosts[0]
templateDoc["replicaSets"][0]["members"][1]["host"] = hosts[1]
templateDoc["replicaSets"][0]["members"][2]["host"] = hosts[2]

#f = open('../files/autoConfigRS.json', 'w+')
#f.write(json.dumps(templateDoc))
#f.close()
