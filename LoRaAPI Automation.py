import urllib.request, json
from urllib.request import Request, urlopen
import urllib
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import json

#req = Request('https://www.postman.com/collections/4ebd5e8ec105c9c245d6/', headers={'User-Agent': 'Mozilla/5.0'})
#webpage = urlopen(req).read()
#print (webpage)

parametersLora = {
    "format":"json",
    "limit":"1000" #limit data yang mau diambil
   # "id": "6e34efc5-2585-461c-bd81-147c801a024c"
}

url = "https://ran.ap.everynet.io/api/v3.0/gateways?format=json"
headers = {"Content-Type": "application/json"}
auth = HTTPBasicAuth('EverynetTelkomNOC@gmail.com', '3veryn@t1')
#files = {'filename': open('filename','rb')}

req = requests.get(url, headers=headers , auth=auth)# , files=files)

LoRa = requests.get(url,headers=headers, auth=auth, params=parametersLora)
print("LoRa status code", LoRa.status_code)

#print(PGN.json())
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
#jprint(LoRa.json())

if(LoRa.status_code == 200):
    print("\nSuccessfully retrieve LoRa data from everynet\n")
else:
    print("\nUnable to retrieve LoRa data with error code " + str(PDAM.status_code) + "\n")

#LoRa = LoRa.json()
#LoRa = LoRa.get('gateways')
jprint(LoRa.json())

Status = []
Sitename = []
Seen = []
Power = []
WWAN = []
Ethernet = []
Lora = []

#PATH = (LoRa.json()).get('gateways')[X]
print( (LoRa.json()).get('gateways')[146].get('lora').get('status'))
print( (LoRa.json()).get('gateways')[146].get('lora_networks')) #kalo gaada data gabisa pake [0]
for x in range(0,5): #5 karna ada 5 module
    if( str( (LoRa.json()).get('gateways')[146].get('modules')[x].get('name') ) == "Ethernet" ):
        print( str((LoRa.json()).get('gateways')[146].get('modules')[x].get('name')) + " " + str((LoRa.json()).get('gateways')[147].get('modules')[x].get('status')) )
        #print( (LoRa.json()).get('gateways')[147].get('modules')[x].get('status') )

Total = 0
ok = 0
warning = 0
error = 0
Ethernet = 0
Lora = 0
Mobile = 0

Gateway = int((LoRa.json()).get('total'))
print(Gateway)
LoraNetwork = len((LoRa.json()).get('gateways')[146].get('lora_networks'))
for x in range(Gateway):
    if( len((LoRa.json()).get('gateways')[x].get('lora_networks'))  > 0 and str((LoRa.json()).get('gateways')[x].get('lora_networks')[0]) == "4"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        Total += 1
    if( str((LoRa.json()).get('gateways')[x].get('system').get('status')) == "warning"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        warning += 1
    if( str((LoRa.json()).get('gateways')[x].get('system').get('status')) == "ok"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        ok += 1
    if( str((LoRa.json()).get('gateways')[x].get('system').get('status')) == "error"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        error += 1
        #print("hehe")
#if( LoraNetwork > 0 ):
#    Total = Total + 1
#    print("hehe")      
      
print("Total Gateway terpasang: ", Total)
print("Total Gateway warning: ", warning)
print("Total Gateway ok: ", ok)
print("Total Gateway error: ", error)







