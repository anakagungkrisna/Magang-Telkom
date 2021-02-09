import urllib.request, json
from urllib.request import Request, urlopen
import urllib
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import json
from urllib import request, parse
import csv

grant_type = 'client_credentials'

#import urllib.request
#weburl = urllib.request.urlopen('https://pgn.antares.id/dashboard/')
#print("result code: " + str(weburl.getcode()))
#data = weburl.read()
#print(data)

#req = Request('https://www.postman.com/collections/4ebd5e8ec105c9c245d6/', headers={'User-Agent': 'Mozilla/5.0'})
#webpage = urlopen(req).read()
#print (webpage)

parameters= {
    "format":"json",
    "limit":"150",
    #"name": "GET ALL DEVICE INFO",
    #"request": {
    #    "auth": {
    #        "bearer": {
    #            "token": "{{token}}"
    #        },
    #        "type": "bearer"
    #    }
    #}
    #"name": "LOGIN USER"
   # "id": "6e34efc5-2585-461c-bd81-147c801a024c"
}

body= {
    'grant_type' : '{}'.format(grant_type),
    #"username":"pegasol",
    #"password":"87c4f0d7"
    "username":"calinmeter",
    "password":"1e06027c"
}

urlLogin = "https://pgn.antares.id/api/pgn/v1/users/login"
urlDeviceInfo = "https://pgn.antares.id/api/pgn/v1/devices/info?row=20&page=1"
urlPostman = "https://www.getpostman.com/collections/4ebd5e8ec105c9c245d6"
headers = {
    "Content-Type": "application/json",
    #"Body": json.dumps({
    #    "username":"pegasol",
    #    "password": "87c4f0d7"
    #}),
    #"Content": {
    #    "method":"post",
    #    "url": "https://pgn.antares.id/api/pgn/v1/users/login"
    #}
}
auth = HTTPBasicAuth('pegasol', '87c4f0d7')
#files = {'filename': open('filename','rb')}


#PGN = requests.get("https://www.postman.com/collections/4ebd5e8ec105c9c245d6", params=parameters)
PGN = requests.post(urlLogin,json=body, headers=headers, auth=auth, params=parameters)
#PDAM = requests.get("https://www.getpostman.com/collections/154df6ec194474004254")
#LoRa = requests.get("https://ran.ap.everynet.io/api/v3.0/gateways?format=json",headers=headers, auth=auth, params=parameters)
print("PGN Login status code", PGN.status_code)
#print("PDAM status code", PDAM.status_code)
#print("LoRa status code", LoRa.status_code)

#print(PGN.json())
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
jprint(PGN.json())

data = (PGN.json()).get('data')
token = data.get('token')
#print(data)
print("Our token: ")
print(token)

headers = {
    "Authorization": "Bearer" + token
}

#Fungsi buat authentification menggunakan bearer token
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

PGN = requests.get(urlDeviceInfo, auth=BearerAuth(token), params=parameters)
print("PGN Device Info status code", PGN.status_code)

#KODE DIBAWAH INI CARA AMBIL DATA SPESIFIK PYTHON
jprint(PGN.json())
PGN = PGN.json()
PGN = PGN.get('data')
#print( PGN.get('data')[1].get('deviceName')) #BEGINI CARA AMBIL DATA SPESIFIK PYTHON

SN = []
accessKey = []
address = []
applicationName = []
createdAt = []
devEUI = []
devId = []
deviceId = []
deviceName = []
hwType = []
latestDownLink = []
latestUpLink = []
latitude = []
longitude = []
organizationName = []

#wholeData = PGN2.json()['data']

with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "accessKey", "address","applicationName","createdAt","devEUI","devId","deviceId","deviceName","hwType","latestDownLink","latestUpLink","latitude","longitude","organizationName"])
        
    numbers = range(0,10)
    for value in numbers:
        #print(PGN.get('data')[value].get('deviceName'))
        SN.append(PGN.get('data')[value].get('SN'))
        SN_ = PGN.get('data')[value].get('SN')
        
        accessKey.append(PGN.get('data')[value].get('accessKey'))
        accessKey_ = PGN.get('data')[value].get('accessKey')
        
        address.append(PGN.get('data')[value].get('address'))
        address_ = PGN.get('data')[value].get('address')
        
        applicationName.append(PGN.get('data')[value].get('applicationName'))
        applicationName_ = PGN.get('data')[value].get('applicationName')
        
        createdAt.append(PGN.get('data')[value].get('createdAt'))
        createdAt_ = PGN.get('data')[value].get('createdAt')
        
        devEUI.append(PGN.get('data')[value].get('devEUI'))
        devEUI_ = PGN.get('data')[value].get('devEUI')
        
        devId.append(PGN.get('data')[value].get('devId'))
        devId_ = PGN.get('data')[value].get('devId')
        
        deviceId.append(PGN.get('data')[value].get('deviceId'))
        deviceId_ = PGN.get('data')[value].get('deviceId')
        
        deviceName.append(PGN.get('data')[value].get('deviceName'))
        deviceName_ = PGN.get('data')[value].get('deviceName')
        hwType.append(PGN.get('data')[value].get('hwType'))
        hwType_ = PGN.get('data')[value].get('hwType')
        
        latestDownLink.append(PGN.get('data')[value].get('latestDownlink'))
        latestDownLink_ = PGN.get('data')[value].get('latestDownlink')
        
        latestUpLink.append(PGN.get('data')[value].get('latestUplink'))
        latestUpLink_ = PGN.get('data')[value].get('latestUplink')
        
        latitude.append(PGN.get('data')[value].get('location').get('latitude'))
        latitude_ = PGN.get('data')[value].get('location').get('latitude')
        
        longitude.append(PGN.get('data')[value].get('location').get('longitude'))
        longitude_ = PGN.get('data')[value].get('location').get('longitude')
        
        organizationName.append(PGN.get('data')[value].get('organizationName'))
        organizationName_ = PGN.get('data')[value].get('organizationName')
        
        writer = csv.writer(file)
        writer.writerow([SN_, accessKey_, address_,applicationName_,createdAt_, devEUI_, devId, deviceId_, deviceName_, hwType_, latestDownLink_, latestUpLink_, latitude_, longitude_, organizationName_])

    

#print(latitude)
#print( PGN.get('data')[1].get('deviceName')) #BEGINI CARA AMBIL DATA SPESIFIK PYTHON


