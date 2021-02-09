from pyzabbix import ZabbixAPI
from html.parser import HTMLParser

import sys
import logging

import requests
import json

import urllib.request, json
from urllib.request import Request, urlopen
import urllib
import requests
from requests.auth import HTTPDigestAuth
import json

#print JSON format 
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


ZABBIX_API_URL = "https://hitrax-zabbix.pins.co.id/zabbix/api_jsonrpc.php"
#ZABBIX_API_URL = "http://139.162.4.139/zabbix/api_jsonrpc.php"
UNAME = "dds-monitor"
PWORD = "dd5gre4t"
#UNAME = "Admin"
#PWORD = "ianganteng"

zapi = ZabbixAPI(ZABBIX_API_URL)
zapi.login(UNAME,PWORD)

application_list = zapi.application.get(
    hostids='10336',
    output="extend",
)
#print(application_list)   
jprint(application_list)


# Get monitoring items
HostID = 10336
print("Get monitoring items from hostids:", HostID)
item_list = zapi.item.get(
    hostids=HostID,
    applicationids='1508',
    output="extend",
)
#print(item_list)
jprint(item_list)

r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "user": UNAME,
                          "password": PWORD},
                      "id": 1,
                      "auth": None
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))

AUTHTOKEN = r.json()["result"] #cara ambil data dari json nya buat dimasukin ke suatu variable

#Retrieving list of host
print("\nRetrieving host:")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "host.get",
                      "params": {
                          "output":[
                                "hostid",
                                "host"
                          ],
                          "selectInterfaces": [
                                "interfaceid",
                                "ip"
                          ]
                  },
                  "id": 2,
                  "auth":AUTHTOKEN
                  })
                 
print(json.dumps(r.json(), indent=4, sort_keys=True))


# Retrieve a list of problems
"""
print("\nRetrieve a list of problems")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "problem.get",
                      "params": {
                          "output": "extend", 
                          "selectAcknowledges": "extend", 
                          "recent": "true", 
                          "sortfield": ["eventid"],
                          "sortorder": "DESC",
                          "name": "status fail"
                      },
                      "id": 2,
                      "auth": AUTHTOKEN
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))
"""

"""
#get history
print("Get item")
r = requests.post(ZABBIX_API_URL,
                json={
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": "extend",
                        "hostids": "10084",
                        "search": {
                            "key_": "system"
                        },
                        "sortfield": "name"
                    },
                    "auth": AUTHTOKEN,
                    "id": 1
                })

print(json.dumps(r.json(), indent=4, sort_keys=True))
"""

#Logout user
print("\nLogout user")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.logout",
                      "params": {},
                      "id": 2,
                      "auth": AUTHTOKEN
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))


#kalau mau konek ke API zabbix, melalui http://.../zabbix/api_jsonrpc.php
zapi = ZabbixAPI("https://hitrax-zabbix.pins.co.id/zabbix/api_jsonrpc.php")
zapi.session.auth = ("dds-monitor", "dd5gre4t")
zapi.login('dds-monitor', 'dd5gre4t')
print("Connected to Zabbix API Version %s" % zapi.api_version())

for h in zapi.host.get(output="extend"):
    print(h['hostid'])














"""
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyzabbix')
log.addHandler(stream)
log.setLevel(logging.DEBUG)
"""
"""
#kalau mau konek ke API zabbix, melalui http://.../zabbix/api_jsonrpc.php
zapi = ZabbixAPI("https://hitrax-zabbix.pins.co.id/zabbix/api_jsonrpc.php")
zapi.session.auth = ("dds-monitor", "dd5gre4t")
zapi.login('dds-monitor', 'dd5gre4t')
print("Connected to Zabbix API Version %s" % zapi.api_version())

for h in zapi.host.get(output="extend"):
    print(h['hostid'])
"""
"""
# Creating an instance of our class.
parser = Parser()
# Poviding the input.
parser.feed(zapi)
print("start tags:", start_tags)
print("end tags:", end_tags)
print("data:", all_data)
print("comments", comments)
"""

"""
zapi = ZabbixAPI("https://hitrax-zabbix.pins.co.id/zabbix/history.php?action=showgraph&itemids%5B%5D=32191")
# Enable HTTP auth
zapi.session.auth = ("dds-monitor", "dd5gre4t")
# Disable SSL certificate verification
zapi.session.verify = False
# Specify a timeout (in seconds)
zapi.timeout = 5.1
# Login (in case of HTTP Auth, only the username is needed, the password, if passed, will be ignored)
zapi.login("dds-monitor", "dd5gre4t")


    """