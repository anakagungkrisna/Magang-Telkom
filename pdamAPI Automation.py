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
    "username":"pdamsemarang",
    "password":"antares2020"
    #"username":"calinmeter",
    #"password":"1e06027c"
}

urlLogin = "https://pdam.antares.id/api/pdam/v1/users/login"
urlDeviceInfo = "https://pdam.antares.id/api/pdam/v1/devices/info?row=20&page=1"
urlPostman = "https://www.getpostman.com/collections/154df6ec194474004254"
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
auth = HTTPBasicAuth('pdamsemarang', 'antares2020')
#files = {'filename': open('filename','rb')}


#PGN = requests.get("https://www.postman.com/collections/4ebd5e8ec105c9c245d6", params=parameters)
PDAM = requests.post(urlLogin,json=body, headers=headers, auth=auth, params=parameters)
#PDAM = requests.get("https://www.getpostman.com/collections/154df6ec194474004254")
#LoRa = requests.get("https://ran.ap.everynet.io/api/v3.0/gateways?format=json",headers=headers, auth=auth, params=parameters)
#print("PDAM Login status code", PDAM.status_code)

print("\n\nOutput: ")
if(PDAM.status_code == 200):
    print("\nSuccessfully logged in to PDAMsemarang and retrieve token")
else:
    print("\nUnable to logged in with error code " + str(PDAM.status_code) )

#print("PDAM status code", PDAM.status_code)
#print("LoRa status code", LoRa.status_code)

#print(PGN.json())
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
#jprint(PDAM.json())

data = (PDAM.json()).get('data')
token = data.get('token')
#print(data)
#print("Our token: ")
#print(token)

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

PDAM = requests.get(urlDeviceInfo, auth=BearerAuth(token), params=parameters)
#print("PDAM Device Info status code", PDAM.status_code)
if(PDAM.status_code == 200):
    print("\nSuccessfully retrieve PDAM Device Info\n")
else:
    print("\nUnable to retrieve PDAM Device Info with error code " + str(PDAM.status_code) + "\n")

#KODE DIBAWAH INI CARA AMBIL DATA SPESIFIK PYTHON
#jprint(PDAM.json())
PDAM = PDAM.json()
PDAM = PDAM.get('data')

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

with open('pdamAPI Automation.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "accessKey", "address","applicationName","createdAt","devEUI","devId","deviceId","deviceName","hwType","latestDownLink","latestUpLink","latitude","longitude","organizationName"])
        
    numbers = range(0,6)
    for value in numbers:
        #print(PGN.get('data')[value].get('deviceName'))
        SN.append(PDAM.get('data')[value].get('SN'))
        SN_ = PDAM.get('data')[value].get('SN')
        
        accessKey.append(PDAM.get('data')[value].get('accessKey'))
        accessKey_ = PDAM.get('data')[value].get('accessKey')
        
        address.append(PDAM.get('data')[value].get('address'))
        address_ = PDAM.get('data')[value].get('address')
        
        applicationName.append(PDAM.get('data')[value].get('applicationName'))
        applicationName_ = PDAM.get('data')[value].get('applicationName')
        
        createdAt.append(PDAM.get('data')[value].get('createdAt'))
        createdAt_ = PDAM.get('data')[value].get('createdAt')
        
        devEUI.append(PDAM.get('data')[value].get('devEui'))
        devEUI_ = PDAM.get('data')[value].get('devEui')
        
        devId.append(PDAM.get('data')[value].get('devId'))
        devId_ = PDAM.get('data')[value].get('devId')
        
        deviceId.append(PDAM.get('data')[value].get('deviceId'))
        deviceId_ = PDAM.get('data')[value].get('deviceId')
        
        deviceName.append(PDAM.get('data')[value].get('deviceName'))
        deviceName_ = PDAM.get('data')[value].get('deviceName')
        hwType.append(PDAM.get('data')[value].get('hwType'))
        hwType_ = PDAM.get('data')[value].get('hwType')
        
        latestDownLink.append(PDAM.get('data')[value].get('latestDownlink'))
        latestDownLink_ = PDAM.get('data')[value].get('latestDownlink')
        
        latestUpLink.append(PDAM.get('data')[value].get('latestUplink'))
        latestUpLink_ = PDAM.get('data')[value].get('latestUplink')
        
        latitude.append(PDAM.get('data')[value].get('location').get('latitude'))
        latitude_ = PDAM.get('data')[value].get('location').get('latitude')
        
        longitude.append(PDAM.get('data')[value].get('location').get('longitude'))
        longitude_ = PDAM.get('data')[value].get('location').get('longitude')
        
        organizationName.append(PDAM.get('data')[value].get('organizationName'))
        organizationName_ = PDAM.get('data')[value].get('organizationName')
        
        writer = csv.writer(file)
        writer.writerow([SN_, accessKey_, address_,applicationName_,createdAt_, devEUI_, devId, deviceId_, deviceName_, hwType_, latestDownLink_, latestUpLink_, latitude_, longitude_, organizationName_])


AS = []
BL = []
DT = []
TS = []
VS = []
deviceID = []
datarate = []
channel = []
rssi = []
snr = []
bandwidth = []
freq = []
spreading = []
modulationType = []
time = []
Type = []
uplinkId = []

#PDAM = PDAM.get('data') #INI PENTING!!!

def buatCSV(deviceEUI): 
    url = "https://pdam.antares.id/api/pdam/v1/uplink/history/" + deviceEUI + "?row=2000&page=1"
    LatestUplink = requests.get(url, auth=BearerAuth(token), params=parameters)
    Latestuplink = LatestUplink.json() #beda di u nya
    
    print("devEUI: " + str(deviceEUI) + " Status code: " + str(LatestUplink.status_code) + " Data caught: " + str(len(Latestuplink.get('data').get('data'))) )
    #jprint(LatestUplink.json())  
    #print(len(LatestUplink.get('data').get('data')))
    LatestUplink = LatestUplink.json()
    #numbers = range(0,694)
    for value in range( len(Latestuplink.get('data').get('data')) ):
        AS.append(LatestUplink.get('data').get('data')[value].get('data').get('AS'))
        AS_ = LatestUplink.get('data').get('data')[value].get('data').get('AS')
          
        BL.append(LatestUplink.get('data').get('data')[value].get('data').get('BL'))
        BL_ = LatestUplink.get('data').get('data')[value].get('data').get('BL')
        
        DT.append(LatestUplink.get('data').get('data')[value].get('data').get('DT'))
        DT_ = LatestUplink.get('data').get('data')[value].get('data').get('DT')
        
        TS.append(LatestUplink.get('data').get('data')[value].get('data').get('TS'))
        TS_ = LatestUplink.get('data').get('data')[value].get('data').get('TS')
        
        VS.append(LatestUplink.get('data').get('data')[value].get('data').get('VS'))
        VS_ = LatestUplink.get('data').get('data')[value].get('data').get('VS')
        
        deviceID.append( LatestUplink.get('data').get('data')[value].get('deviceId'))
        deviceID_ = LatestUplink.get('data').get('data')[value].get('deviceId')
        
        datarate.append(LatestUplink.get('data').get('data')[value].get('radio').get('datarate'))
        datarate_ = LatestUplink.get('data').get('data')[value].get('radio').get('datarate')
        
        channel.append( LatestUplink.get('data').get('data')[value].get('radio').get('hardware').get('channel'))
        channel_ = LatestUplink.get('data').get('data')[value].get('radio').get('hardware').get('channel')
        
        rssi.append( LatestUplink.get('data').get('data')[value].get('radio').get('hardware').get('rssi'))
        rssi_ = LatestUplink.get('data').get('data')[value].get('radio').get('hardware').get('rssi')
        
        snr.append( LatestUplink.get('data').get('data')[value].get('radio').get('hardware').get('snr'))
        snr_ = LatestUplink.get('data').get('data')[value].get('radio').get('hardware').get('snr')
        
        bandwidth.append( LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('bandwidth'))
        bandwidth_ = LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('bandwidth')
        
        freq.append( LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('freq'))
        freq_ = LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('freq')
        
        spreading.append( LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('spreading'))
        spreading_ = LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('spreading')
        
        modulationType.append( LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('type'))
        modulationType_ = LatestUplink.get('data').get('data')[value].get('radio').get('modulation').get('type')
        
        time.append( LatestUplink.get('data').get('data')[value].get('time'))
        time_ = LatestUplink.get('data').get('data')[value].get('time')
        
        Type.append( LatestUplink.get('data').get('data')[value].get('type'))
        Type_ = LatestUplink.get('data').get('data')[value].get('type')
        
        uplinkId.append( LatestUplink.get('data').get('data')[value].get('uplinkId'))
        uplinkId_ = LatestUplink.get('data').get('data')[value].get('uplinkId')
        
    #numbers = range(0,2000)
    #for value in numbers:
        writer = csv.writer(file)
        writer.writerow([AS_, BL_, DT_,TS_,VS_, deviceID_, datarate_, channel_, rssi_, snr_, bandwidth_, freq_, spreading_, modulationType_, time_, Type_, uplinkId_])
    




numbers = range(0,6)
for x in numbers:
    with open(devEUI[x] + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["AS", "BL", "DT","TS","VS","deviceId","datarate","channel","rssi","snr","bandwidth","freq","spreading","ModulationType","time","type","uplinkId"])
        buatCSV(devEUI[x])

