import urllib.request, json
from urllib.request import Request, urlopen
import urllib
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import json
from urllib import request, parse
import csv
from datetime import date
import datetime

grant_type = 'client_credentials'

def buatCSV(deviceEUI):

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

    url = "https://pgn.antares.id/api/pgn/v1/uplink/history/" + deviceEUI + "/la"
    LatestUplink = requests.get(url, auth=BearerAuth(token), params=parameters)
    print("Latest Uplink status code for devEUI: " + str(deviceEUI) + " is " + str(LatestUplink.status_code) )
    #jprint(LatestUplink.json())  
    LatestUplink = LatestUplink.json()
    
    AS.append(LatestUplink.get('data')[0].get('data').get('AS'))
    AS_ = LatestUplink.get('data')[0].get('data').get('AS')
    
    BL.append(LatestUplink.get('data')[0].get('data').get('BL'))
    BL_ = LatestUplink.get('data')[0].get('data').get('BL')
    
    DT.append(LatestUplink.get('data')[0].get('data').get('DT'))
    DT_ = LatestUplink.get('data')[0].get('data').get('DT')
    
    TS.append(LatestUplink.get('data')[0].get('data').get('TS'))
    TS_ = LatestUplink.get('data')[0].get('data').get('TS')
    
    VS.append(LatestUplink.get('data')[0].get('data').get('VS'))
    VS_ = LatestUplink.get('data')[0].get('data').get('VS')
    
    deviceID.append( LatestUplink.get('data')[0].get('deviceId') )
    deviceID_ = LatestUplink.get('data')[0].get('deviceId')
    
    datarate.append(LatestUplink.get('data')[0].get('radio').get('datarate'))
    datarate_ = LatestUplink.get('data')[0].get('radio').get('datarate')
    
    channel.append( LatestUplink.get('data')[0].get('radio').get('hardware').get('channel') )
    channel_ = LatestUplink.get('data')[0].get('radio').get('hardware').get('channel')
    
    rssi.append( LatestUplink.get('data')[0].get('radio').get('hardware').get('rssi') )
    rssi_ = LatestUplink.get('data')[0].get('radio').get('hardware').get('rssi')
    
    snr.append( LatestUplink.get('data')[0].get('radio').get('hardware').get('snr') )
    snr_ = LatestUplink.get('data')[0].get('radio').get('hardware').get('snr')
    
    bandwidth.append( LatestUplink.get('data')[0].get('radio').get('modulation').get('bandwidth') )
    bandwidth_ = LatestUplink.get('data')[0].get('radio').get('modulation').get('bandwidth')
    
    freq.append( LatestUplink.get('data')[0].get('radio').get('modulation').get('freq') )
    freq_ = LatestUplink.get('data')[0].get('radio').get('modulation').get('freq')
    
    spreading.append( LatestUplink.get('data')[0].get('radio').get('modulation').get('spreading') )
    spreading_ = LatestUplink.get('data')[0].get('radio').get('modulation').get('spreading')
    
    modulationType.append( LatestUplink.get('data')[0].get('radio').get('modulation').get('type') )
    modulationType_ = LatestUplink.get('data')[0].get('radio').get('modulation').get('type')
    
    time.append( LatestUplink.get('data')[0].get('time') )
    time_ = LatestUplink.get('data')[0].get('time')
    
    Type.append( LatestUplink.get('data')[0].get('type') )
    Type_ = LatestUplink.get('data')[0].get('type')
    
    uplinkId.append( LatestUplink.get('data')[0].get('uplinkId') )
    uplinkId_ = LatestUplink.get('data')[0].get('uplinkId')
    
    writer = csv.writer(file)
    writer.writerow([AS_, BL_, DT_,TS_,VS_, deviceID_, datarate_, channel_, rssi_, snr_, bandwidth_, freq_, spreading_, modulationType_, time_, Type_, uplinkId_])   

"""
numbers = range(0,10)
for x in numbers:
    with open(devEUI[x] + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["AS", "BL", "DT","TS","VS","deviceId","datarate","channel","rssi","snr","bandwidth","freq","spreading","ModulationType","time","type","uplinkId"])
        buatCSV(devEUI[x])
"""    

#print(PGN.json())
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
#Fungsi buat authentification menggunakan bearer token
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
        
def LOGINandGETDATA(Username,Password):
    
    parameters= {
        "format":"json",
        "limit":"150",
    }
    
    body= {
        'grant_type' : '{}'.format(grant_type),
        "username":Username,
        "password":Password
    }
    
    headers = {
        "Content-Type": "application/json",
    }
    
    auth = HTTPBasicAuth(Username, Password)
    Request = requests.post(urlLogin,json=body, headers=headers, auth=auth, params=parameters)
    
    print(Username,"Login status code", Request.status_code)
    
    data = (Request.json()).get('data')
    token = data.get('token')

    headers = {
        "Authorization": "Bearer" + token
    }

    Request = requests.get(urlDeviceInfo, auth=BearerAuth(token), params=parameters)
    print(Username, "Device Info status code", Request.status_code)

    Request = Request.json()
    Request = Request.get('data')
    return Request.get('data'), Request.get('totalDevices')


def gantiFormatWaktu(Waktu):

    waktu = datetime.datetime.strptime(Waktu,"%Y-%m-%dT%H:%M:%S.%fZ")
    jam = 7
    jamTambah = datetime.timedelta(hours=jam)
    
    waktuAsli = waktu + jamTambah
    
    formatTanggal = "%d-%m-%Y"
    formatJam = "%H:%M:%S"
    Tanggal = waktuAsli.strftime(formatTanggal)
    Jam = waktuAsli.strftime(formatJam) 
    waktu = Tanggal +" "+ Jam
    
    return Tanggal, Jam, waktu

def cekWaktu(Waktu):
    #Declare our date varaibles
    waktuDevice = Waktu
    sekarang = datetime.datetime.now()
    #calculate the difference
    timediff = sekarang - waktuDevice 
    #print(timediff)
    #convert to seconds
    seconds = timediff.total_seconds()   
    #print(seconds)
    #Convert seconds to hours (there are 3600 seconds in an hour)
    hours = seconds/3600   
    #Show the total
    return hours
    
def getDataLora():

    parametersLora = {
        "format":"json",
        "limit":"1000" #limit data yang mau diambil
    }
    
    auth = HTTPBasicAuth('EverynetTelkomNOC@gmail.com', '3veryn@t1')
    
    headers = {"Content-Type": "application/json"}

    LoRa = requests.get(urlLora,headers=headers, auth=auth, params=parametersLora)
    print("LoRa status code", LoRa.status_code)       

    
def detailError(allDevice, deviceName):
    
    headers = {
        "X-M2M-Origin": "nociot:247365",
        "Content-Type": "application/json;ty=4",
        "Accept": "application/json"
    }
    
    for j in range(len(allDevice)):
        if( allDevice[j].get('deviceName') == deviceName):
            print(allDevice[j].get('deviceName') + "(" + str(allDevice[j].get('devEui')) + ") " + "Meter Status: Disconnected")
            time = gantiFormatWaktu(allDevice[j].get('latestUplink'))
            print("Dashboard: Last update " + time[2] )
            print("NS: ")
            
            urlLogin = "https://platform.antares.id:8443/~/antares-cse/antares-id/" + str(allDevice[j].get('applicationName')) + "/la"
            Request = requests.get(urlLogin,headers=headers)
            #print("Postman status code", Request.status_code)
            #jprint(Request.json())
            
            print("Antares API(Postman): " + str(datetime.datetime.strptime((Request.json()).get('m2m:cin').get('lt'),"%Y%m%dT%H%M%S"))+ " (" + (Request.json()).get('m2m:cin').get('lt') + ")" )
            print("PGN Availability: ")
            
            dataCON = json.loads((Request.json()).get('m2m:cin').get('con')) #buat dapetin data dari json string (contoh pada postman bagian con

            #Buat iterate key dari json string
            #print(dataCON['gateway']) 
            #pairs = jsonObject.items()
            #for key, value in pairs:
            #    print(value)
            

            
            print("Gateway: (" + dataCON['gateway'] + ")\n" )

urlLogin = "https://pgn.antares.id/api/pgn/v1/users/login"
urlDeviceInfo = "https://pgn.antares.id/api/pgn/v1/devices/info?row=20&page=1"
urlLatestUplink = "https://pgn.antares.id/api/pgn/v1/uplink/history/{{devEUI}}/la"
urlPostman = "https://www.getpostman.com/collections/4ebd5e8ec105c9c245d6"
applicationName = "isi application name disini"
urlAntaresPostman = "https://platform.antares.id:8443/~/antares-cse/antares-id/" + applicationName + "/la"
urlLora = "https://ran.ap.everynet.io/api/v3.0/gateways?format=json"


#files = {'filename': open('filename','rb')}

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
    "username":"pegasol",
    "password":"87c4f0d7"
    #"username":"calinmeter",
    #"password":"1e06027c"
}


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

jprint(PGN.json())

data = (PGN.json()).get('data')
token = data.get('token')
#print(data)
print("Our token: ")
print(token)

headers = {
    "Authorization": "Bearer" + token
}

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
totalDevice = int(PGN.get('totalDevices'))
#wholeData = PGN2.json()['data']

with open('pgnAPI Automation.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "accessKey", "address","applicationName","createdAt","devEUI","devId","deviceId","deviceName","hwType","latestDownLink","latestUpLink","latitude","longitude","organizationName"])
        
    #numbers = range(0,10)
    for value in range(totalDevice):
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
        
        devEUI.append(PGN.get('data')[value].get('devEui'))
        devEUI_ = PGN.get('data')[value].get('devEui')
        
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
  
  
######################################Wira Energi#######################

wiraEnergi, totalWira = LOGINandGETDATA("wiraenergi","c6b275e8")
jprint(wiraEnergi)
#print(totalWira)

wiraApplicationName = []
wiraDevEUI = []
wiraDeviceName = []
wiraLatestUpLink = []
wiraTanggal = []
wiraJam = []
wiraWaktu = []
wiraOrganizationName = []

wiraConnected = 0
wiraOk = []
wiraDisconnected = 0
wiraError = []

for value in range(totalWira):   
    wiraApplicationName.append(wiraEnergi[value].get('applicationName'))   
    wiraDevEUI.append(wiraEnergi[value].get('devEui'))
    wiraDeviceName.append(wiraEnergi[value].get('deviceName'))
    wiraLatestUpLink.append(wiraEnergi[value].get('latestUplink'))
    wiraOrganizationName.append(wiraEnergi[value].get('organizationName'))

for x in range(len(wiraLatestUpLink)):
    if(wiraLatestUpLink[x] == None): print("no latest uplink")
    else:
        #for i in range(10,100,10): #kenapa 10,100,10?
        a = gantiFormatWaktu(wiraLatestUpLink[x]) # The output of the function is a tuple, which we put in "a"

        wiraTanggal.append(a[0])
        wiraJam.append(a[1])
        wiraWaktu.append(a[2])

        print(wiraDeviceName[x], wiraWaktu[x])

    
now = datetime.datetime.now()
print ("\nCurrent date and time : ", now.strftime("%d-%m-%Y %H:%M:%S"))

for x in range(len(wiraWaktu)):
    wiraWaktu[x] = datetime.datetime.strptime(wiraWaktu[x], '%d-%m-%Y %H:%M:%S') #ubah wiraWaktu jadi datetime object

for x in range(len(wiraLatestUpLink)):
    
    if(wiraLatestUpLink[x] == None): print("Device error")
    else:
        hasil = cekWaktu(wiraWaktu[x])
        #print(hasil)
        if (hasil > 24):
            #print('24 hours have passed')
            wiraDisconnected += 1
            wiraError.append(wiraDeviceName[x])
        else:
            #print('Date is within 24 hours!')  
            wiraConnected += 1
            wiraOk.append(wiraDeviceName[x])

print("Wiraenergi: " + str(wiraConnected) + "N|" + str(wiraDisconnected) + "M" )

print("\nError message:")
for i in range(len(wiraError)):
    detailError(wiraEnergi, wiraError[i])

#print(latitude)
#print( PGN.get('data')[1].get('deviceName')) #BEGINI CARA AMBIL DATA SPESIFIK PYTHON


