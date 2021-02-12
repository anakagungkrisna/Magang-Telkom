import urllib.request, json
from urllib.request import Request, urlopen
import urllib
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import json

import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile

import os.path



parametersLora = {
    "format":"json",
    "limit":"1000" #limit data yang mau diambil
   # "id": "6e34efc5-2585-461c-bd81-147c801a024c"
}

url = "https://ran.ap.everynet.io/api/v3.0/gateways?format=json"
headers = {"Content-Type": "application/json"}
auth = HTTPBasicAuth('EverynetTelkomNOC@gmail.com', '3veryn@t1')
#files = {'filename': open('filename','rb')}

#req = requests.get(url, headers=headers , auth=auth)# , files=files)

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

#JANGAN DIHAPUS! DOKUMENTASI ITU
#PATH = (LoRa.json()).get('gateways')[X]
#print( (LoRa.json()).get('gateways')[146].get('lora').get('status'))
#print( (LoRa.json()).get('gateways')[146].get('lora_networks')) #kalo gaada data gabisa pake [0]
#for x in range(0,5): #5 karna ada 5 module
#    if( str( (LoRa.json()).get('gateways')[146].get('modules')[x].get('name') ) == "Ethernet" ):
#        print( str((LoRa.json()).get('gateways')[146].get('modules')[x].get('name')) + " " + str((LoRa.json()).get('gateways')[147].get('modules')[x].get('status')) )
#        print( (LoRa.json()).get('gateways')[147].get('modules')[x].get('status') )

Total = 0
ok = 0
warning = 0
error = 0
Ethernet = 0
Lora = 0
Mobile = 0
gatewayError = []
gatewayDown = []
gatewayUp = []

Gateway = int((LoRa.json()).get('total')) #seluruh Gateway yang didapat dari website everynet
#print(Gateway)
#LoraNetwork = len((LoRa.json()).get('gateways')[146].get('lora_networks'))
LoRa = LoRa.json() #Kalo yang LoRa diganti LoRa.json() jadi jauh lebih lambat!
for x in range(Gateway):
    if( len((LoRa).get('gateways')[x].get('lora_networks'))  > 0 and str((LoRa).get('gateways')[x].get('lora_networks')[0]) == "4"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        Total += 1
        if( str((LoRa).get('gateways')[x].get('system').get('status')) == "warning" or str((LoRa).get('gateways')[x].get('system').get('status')) == "warning_power"): 
            warning += 1
        if( str((LoRa).get('gateways')[x].get('system').get('status')) == "ok"): 
            ok += 1
        #if( str((LoRa).get('gateways')[x].get('system').get('status')) == "error"): #Error itu ketika status error dan power error
        #    error += 1
        #for y in range(0,5): #5 karna ada 5 module
        #    if( str( (LoRa).get('gateways')[x].get('modules')[y].get('name') ) == "Power" and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
        #        error += 1
        if( str((LoRa).get('gateways')[x].get('system').get('status')) == "error_power" or str((LoRa).get('gateways')[x].get('system').get('status')) == "error" or str((LoRa).get('gateways')[x].get('system').get('status')) == "error_recovery"): #Error itu ketika status error dan power error
            error += 1
            gatewayError.append( str(LoRa.get('gateways')[x].get('sitename')) )
    
        #print("hehe")
#if( LoraNetwork > 0 ):
#    Total = Total + 1
#    print("hehe")      

dataset = pd.DataFrame(gatewayError, columns = ["Nama Gateway Error"]) #DATA GATEWAY DOWN SAAT ITU
print("\n Nama Gateway error: ")
print(dataset)



if os.path.isfile('dataset.xlsx'):
    print ("\n\nDataset is present")
    print ("Reading from dataset..")
    data = pd.read_excel('dataset.xlsx', index_col=None, na_values=['NA'], usecols = "B") #DATA GATEWAY DOWN SEJAM SEBELUM

    errorBanding = pd.concat([data['Nama Gateway Error'],dataset['Nama Gateway Error']]).drop_duplicates(keep=False)
    errorBanding = errorBanding.reset_index() #buat kolom index, reset index pembeda keseluruhan
    print(errorBanding)

    #Cek apakah pada errorBanding terdapat kesamaan data pada gatewayError(dataset), yang menandakan gateway down
    x = 0
    y = 0
    for x in range(len(errorBanding)): #Perbedaan antara gateway sebelum (dataset) dengan gateway sesudah (data)
        for y in range(len(dataset)): #Gateway error saat itu
            #print("hehe")
            if( errorBanding.loc[x,'Nama Gateway Error'] == dataset.loc[y,'Nama Gateway Error'] ):
                gatewayDown.append(str(errorBanding.loc[x,'Nama Gateway Error']))
                break
            else: 
                continue
    #Cek apakah pada errorBanding terdapat kesamaan data pada data, yang menandakan gateway Up
    x = 0
    y = 0
    for x in range(len(errorBanding)): #Perbedaan antara gateway sebelum (dataset) dengan gateway sesudah (data)
        for y in range(len(data)): #Gateway error saat itu
            #print("hehe")
            if( errorBanding.loc[x,'Nama Gateway Error'] == data.loc[y,'Nama Gateway Error'] ):
                gatewayUp.append(str(errorBanding.loc[x,'Nama Gateway Error']))
                break
            else: 
                continue
    #x = 0
    #for x in range(len(errorBanding)):
    #    perbandingan.loc[x,'Pembeda'] = errorBanding.loc[x,0]

    #for i in range(len(data)):
    #    for x in range(Gateway):
    #        if( data.loc[x, 'Nama Gateway Error'] == str(LoRa.get('gateways')[x].get('sitename')) ): 

    #print(data)
    print("\t\t*Output*")
    print("Total Gateway terpasang: ", Total)
    print("Total Gateway warning: ", warning)
    print("Total Gateway ok: ", ok)
    print("Total Gateway error: ", error)
    print("\nGateway Down: ")
    print(gatewayDown)
    print("\nGateway Up: ")
    print(gatewayUp)
    dataset.to_excel("dataset.xlsx")
    print("\nDataset has been updated")
    print("Thank you for using this program :)")

else:
    print("Dataset is not yet created")
    print("Creating Dataset now..")
    dataset.to_excel("dataset.xlsx")
    print("Dataset has been created")
    print("You can run again this program to get the output")
