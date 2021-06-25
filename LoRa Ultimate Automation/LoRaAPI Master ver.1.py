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
import shutil, os

import datetime
from datetime import date
import time

# importing all required libraries for telegram bot
import sys
import telebot 
from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient, sync, events 
import telegram

from apscheduler.schedulers.blocking import BlockingScheduler
import schedule



# get your api_id, api_hash, token 
api_id = 3083142
api_hash = '0ad118c0b09254087844b062ef3f4a14'
token = '1665551618:AAFvpiCLP19vYNPVez0-wlNFdcEe8HlK2Jw'
groupid = '-241710910'
NOCid = '-1001249682496'
  
# your phone number 
phone = '6281319771165'

def reLogin():
    client = TelegramClient('session', api_id, api_hash)
    #client.connect()
    client.start() #ini harus pake start. connect bisa kalo untuk akun sendiri.
    print("Resetting telegram session")

    laporanPukul = datetime.datetime.now().strftime('%H.%M.%S (%d-%m-%Y)') #Buat Judul Laporan Telegram  

    #name = 'No. Telepon NOC.txt'
    #path = 'C:/Users/t/Documents/LoRa Ultimate Automation/' + name
    #files = {'document':open(path,'rb')}
    #f = open('No. Telepon NOC.txt','r')
    #resp = requests.post('https://api.telegram.org/bot1665551618:AAFvpiCLP19vYNPVez0-wlNFdcEe8HlK2Jw/sendDocument?chat_id=-241710910&caption=All_Gateway_Down_Detail_at: {}'.format(laporanPukul), files = f)
    #f.close()
    #print(files.closed)

    #message = "MUHEHE" + "HAHA"
    #send_message(groupid, token, message)

    client.disconnect()
    print("Successfully resetting telegram session")

def send_message(GroupID, Token, context):
    bot = telegram.Bot(Token)
    bot.sendMessage(GroupID,context)
    
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#Masih dalam development
j = 0  
def debugGateway(num, mac, Sitename):
    global j
    if( str((LoRa).get('gateways')[num].get('mac')) == mac or str((LoRa).get('gateways')[num].get('sitename')) == Sitename ): 
        jprint((LoRa).get('gateways')[num])
    
    #cek existence data2 nya.
        typedModules= (LoRa).get('gateways')[num].get('modules')  #dump buat ubah dict jadi string, karna json.load perlu input string
        while j < len(typedModules):
            if(typedModules[j].get('type') == "power" ): print("power exist")
            if(typedModules[j].get('type') == "eth"): print("ethernet exist")
            if(typedModules[j].get('type') == "wwan"): print("mobile exist")
            j += 1
    j = 0

def dhms_from_seconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)

def lamaWaktuDown(Waktu):
    #Declare our date varaibles
    waktuDevice = Waktu
    sekarang = datetime.datetime.now()
    #calculate the difference
    timediff = sekarang - waktuDevice 
    #print(timediff)
    #convert to seconds
    seconds = timediff.total_seconds()   
    #days = timediff.total_days()
    #print(seconds)
    #Convert seconds to hours (there are 3600 seconds in an hour)
    hours = seconds/3600 
    #days = seconds/86400
    #Show the total
    return seconds#hours
 

satuHariKebawah = []
satuHariKeatas = []
tigaHariKeatas = []
variabelWaktu = []
variabelNama = []

def cekDetailError(LoRa, num, Sitename, tipe):
    k = 0
    global variabelWaktu
    cekPower = False
    cekEther = False
    cekMobile = False
    cekLora = False
    hasilEther = ""
    hasilPower = ""
    hasilMobile = ""
    hasilLora = ""
    waktu = ""
    if(tipe == "Down"): 
        if( str((LoRa).get('gateways')[num].get('sitename')) == Sitename ): 
        
            #debugGateway(num, None, Sitename)
        
            waktu = datetime.datetime.strptime((LoRa).get('gateways')[num].get('seen'),"%Y-%m-%dT%H:%M:%S.%fZ")
            jam = 7
            jamTambah = datetime.timedelta(hours=jam)
            
            waktuAsli = waktu + jamTambah
            
            formatTanggal = "%d-%m-%Y"
            formatJam = "%H:%M:%S"
            Tanggal = waktuAsli.strftime(formatTanggal)
            Jam = waktuAsli.strftime(formatJam)   

            lamaHariDown = str(int(dhms_from_seconds(lamaWaktuDown(waktuAsli))[0]))
            lamaJamDown = str(int(dhms_from_seconds(lamaWaktuDown(waktuAsli))[1]))
            lamaMenitDown = str(int(dhms_from_seconds(lamaWaktuDown(waktuAsli))[2]))
            lamaDetikDown = str(int(dhms_from_seconds(lamaWaktuDown(waktuAsli))[3]))
            
            variabelWaktu.append(int(lamaWaktuDown(waktuAsli)))
            variabelNama.append(Sitename)
            #print(variabelWaktu)
            
            

            #Jam = Jam + jamTambah
            
            #waktu = str((LoRa).get('gateways')[num].get('seen'))
            #waktu = waktu.split(".")
            #waktu = waktu[0].split("T")
            
            #jprint((LoRa).get('gateways')[num].get('modules'))           
            
            got = 0
            #cek existence data2 nya.
            if( (LoRa).get('gateways')[num].get('lora').get('status') == "ok" ): 
                cekLora = True
                #got += 1
            """
            got = 0 
            y = 0
            while y < len((LoRa).get('gateways')[num].get('modules')): #ada 6 module, ada juga yg 5
                if( str( (LoRa).get('gateways')[num].get('modules')[y].get('type') ) == "power" and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "ok" ) :
                    cekPower = True
                    got += 1
                if( str( (LoRa).get('gateways')[num].get('modules')[y].get('type') ) == "eth" and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "ok" ):
                    cekEther = True
                    got += 1
                if( str( (LoRa).get('gateways')[num].get('modules')[y].get('type') ) == "wwan" and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "ok" ):
                    cekMobile = True#print("mobile exist")
                    got += 1
                if( str( (LoRa).get('gateways')[num].get('modules')[y].get('type') ) == "" and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "ok" ):
                    cekPower = True
                    got += 1
                #if( str( (LoRa).get('gateways')[num].get('modules')[y].get('type') ) == "" and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                #    cekPower = False
                    #got += 1
                if(y == len((LoRa).get('gateways')[num].get('modules')) - 1):
                    #if( str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == ""):
                        #excelPower.append( str( (LoRa).get('gateways')[x].get('modules')[y].get('status')) )
                    if(got == 0): 
                        cekPower = False                   
                        cekEther = False
                        cekMobile = False
                    if(got == 1 and cekPower == True):
                        cekEther = False
                        cekMobile = False
                    if(got == 1 and cekEther == True):
                        cekPower = False
                        cekMobile = False
                    if(got == 1 and cekMobile == True):
                        cekPower = False
                        cekEther = False 
                    if(got == 2 and cekPower == True and cekEther == True): 
                        cekMobile = False
                    if(got == 2 and cekPower == True and cekMobile == True): 
                        cekEther = False
                    if(got == 2 and cekEther == True and cekMobile == True): 
                        cekPower = False
                    if(got == 3): pass
                y += 1
            """
            
            typedModules= (LoRa).get('gateways')[num].get('modules')  #dump buat ubah dict jadi string, karna json.load perlu input string
            while k < len(typedModules):
                if(typedModules[k].get('type') == "power" and typedModules[k].get('status') == "ok" ): 
                    cekPower = True#print("power exist")
                    got += 1
                if(typedModules[k].get('type') == "eth" and typedModules[k].get('status') == "ok"): 
                    cekEther = True#print("ethernet exist")
                    got += 1
                if(typedModules[k].get('type') == "wwan" and typedModules[k].get('status') == "ok"): 
                    cekMobile = True#print("mobile exist")
                    got += 1
                #if(typedModules[k].get('type') == "" and typedModules[k].get('status') == "ok" ): 
                #    cekPower = True
                
                k += 1
            k = 0  
          
            
            if(got == 0): 
                cekPower = False
                cekEther = False
                cekMobile = False
            if(got == 1 and cekPower == True):
                cekEther = False
                cekMobile = False
            if(got == 1 and cekEther == True):
                #print( (LoRa).get('gateways')[num].get('Sitename') )
                cekPower = False
                cekMobile = False
            if(got == 1 and cekMobile == True):
                #print( (LoRa).get('gateways')[num].get('Sitename') )
                cekPower = False
                cekEther = False 
            if(got == 2 and cekPower == True and cekEther == True): cekMobile = False
            if(got == 2 and cekPower == True and cekMobile == True): cekEther = False
            if(got == 2 and cekEther == True and cekMobile == True): 
                #print( (LoRa).get('gateways')[num].get('Sitename') )
                cekPower = False
            if(got == 3): pass#print( (LoRa).get('gateways')[num].get('Sitename') )
                
            got = 0  
            
            if((LoRa).get('gateways')[num].get('Sitename') == "Tower STO KLG 2.1" ): #ini karna ada 1 gateway yg memang gaada mobile nya.
                mob = False  
                
            
            if(cekPower == False): hasilPower = "Power, "
            else: hasilPower = ""
            if(cekEther == False): hasilEther = "Ethernet, "
            else: hasilEther = ""
            if(cekMobile == False): hasilMobile = "Mobile, "
            else: hasilMobile = ""
            if(cekLora == False): hasilLora = "Lora "
            else: hasilLora = ""
        
            Detail = "- " + Sitename + " Down (" + hasilPower + hasilEther + hasilMobile + hasilLora + "error)" + " pukul " + Jam + " (" +  Tanggal + ")" + " selama " + lamaHariDown + "d" + lamaJamDown + "h" + lamaMenitDown + "m" + lamaDetikDown + "s"
            
            if(int(lamaHariDown) < 1): satuHariKebawah.append(Detail)
            if(int(lamaHariDown) >= 1 and int(lamaHariDown) < 3): satuHariKeatas.append(Detail)
            else: tigaHariKeatas.append(Detail)
            
            return Detail
            
        else: pass
        
    if(tipe == "Up"):
        if( str((LoRa).get('gateways')[num].get('sitename')) == Sitename ): 
            waktu = datetime.datetime.strptime((LoRa).get('gateways')[num].get('seen'),"%Y-%m-%dT%H:%M:%S.%fZ")
            jam = 7
            jamTambah = datetime.timedelta(hours=jam)
            
            waktuAsli = waktu + jamTambah
            
            formatTanggal = "%d-%m-%Y"
            formatJam = "%H:%M:%S"
            Tanggal = waktuAsli.strftime(formatTanggal)
            Jam = waktuAsli.strftime(formatJam)   
            
            Detail = "- " + Sitename + " Up pukul " + Jam + " (" + Tanggal + ")"
             
            return Detail
            
        else: pass
        
    return None


def bubble_sort(nums, names):
    # We set swapped to True so the loop looks runs at least once
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                # Swap the elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                names[i], names[i+1] = names[i+1], names[i]
                # Set the flag to True so we'll loop again
                swapped = True
                
    

    
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

excelStatus = []
excelMAC = []
excelSitename = []   
excelVendor = []
excelGeoposition = []
excelUptime = []
excelSeen = []
excelPower = []
excelWWAN = []
excelEthernet = []
excelGNSS = []
excelMonitoring = []
excelControl = []
excelLoRa = []


def buatExcel(json):
    cekPower = False
    cekEther = False
    cekMobile = False
    cekLora = False
    

    Gateway = int((json).get('total'))
    
    for x in range(Gateway):
        arrGateway = (json).get('gateways')[x].get('lora_networks')
        gatewayTrue = "4" in arrGateway
        #print(gatewayTrue)
    
        #if( len((LoRa).get('gateways')[x].get('lora_networks'))  > 0 and str((LoRa).get('gateways')[x].get('lora_networks')[0]) == "4"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        if(gatewayTrue == True): 
            #Total += 1
            excelSitename.append( str((json).get('gateways')[x].get('sitename')) )
            excelStatus.append( str((json).get('gateways')[x].get('system').get('status')) )
            excelMAC.append( str((json).get('gateways')[x].get('mac')) )
            excelVendor.append( str((json).get('gateways')[x].get('system').get('vendor')) )
            excelGeoposition.append( str((json).get('gateways')[x].get('geoposition').get('country')) + ">" + str((json).get('gateways')[x].get('geoposition').get('city')) )
            excelUptime.append("NONE")
            waktu = gantiFormatWaktu( str((json).get('gateways')[x].get('seen')) )
            excelSeen.append(waktu[2])
            
            ##################### ALGORITMA PEMBUATAN EXCEL WEBSITE EVERYNET!!! (PALING BERHARGA)############################
            got = 0 
            y = 0
            while y < len((json).get('gateways')[x].get('modules')): #ada 6 module, ada juga yg 5
                if( (str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "power" ) ) :
                    excelPower.append( str( (json).get('gateways')[x].get('modules')[y].get('status')) )  
                    cekPower = True
                    got += 1
                if( (str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "eth" )):
                    excelEthernet.append( str( (json).get('gateways')[x].get('modules')[y].get('status')) )
                    cekEther = True
                    got += 1
                if( (str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "wwan" )):
                    excelWWAN.append( str( (json).get('gateways')[x].get('modules')[y].get('status')) )
                    cekMobile = True#print("mobile exist")
                    got += 1
                if( (str( (json).get('gateways')[x].get('modules')[y].get('name') ) == "GNSS" )):
                    excelGNSS.append( str( (json).get('gateways')[x].get('modules')[y].get('status')) )
                if( str( (json).get('gateways')[x].get('modules')[y].get('type') ) == ""):
                    excelPower.append( str( (json).get('gateways')[x].get('modules')[y].get('status')) )
                    cekPower = True
                    got += 1
                if(y == len((json).get('gateways')[x].get('modules')) - 1):
                    #if( str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == ""):
                        #excelPower.append( str( (LoRa).get('gateways')[x].get('modules')[y].get('status')) )
                    if(got == 0): 
                        cekPower = False
                        excelPower.append("-")                     
                        cekEther = False
                        excelEthernet.append("-") 
                        cekMobile = False
                        excelWWAN.append("-") 
                    if(got == 1 and cekPower == True):
                        cekEther = False
                        excelEthernet.append("-") 
                        cekMobile = False
                        excelWWAN.append("-") 
                    if(got == 1 and cekEther == True):
                        cekPower = False
                        excelPower.append("-")
                        cekMobile = False
                        excelWWAN.append("-")
                    if(got == 1 and cekMobile == True):
                        cekPower = False
                        excelPower.append("-")
                        cekEther = False 
                        excelEthernet.append("-")
                    if(got == 2 and cekPower == True and cekEther == True): 
                        cekMobile = False
                        excelWWAN.append("-")
                    if(got == 2 and cekPower == True and cekMobile == True): 
                        cekEther = False
                        excelEthernet.append("-") 
                    if(got == 2 and cekEther == True and cekMobile == True): 
                        cekPower = False
                        excelPower.append("-")
                    if(got == 3): pass
                y += 1
            
            
                
            excelMonitoring.append("NONE")
            excelControl.append("NONE")             
            excelLoRa.append( (json).get('gateways')[x].get('lora').get('status') )
                
                
    excelData = {'Status': excelStatus,
        'MAC': excelMAC,
        'Sitename': excelSitename,
        'Vendor': excelVendor,
        'Geoposition': excelGeoposition,
        'Uptime': excelUptime,
        'Seen': excelSeen,
        'Power': excelPower,
        'WWAN': excelWWAN,
        'Ethernet': excelEthernet,
        'GNSS': excelGNSS,
        'LoRa': excelLoRa
        }
        
    
    #dataStatus = dataStatus.transpose()
    #ExcelFile = pd.DataFrame([[excelStatus], [excelMAC], [excelSitename], [excelVendor], [excelGeoposition], [excelUptime], [excelSeen] ], columns = [["Status"], ["MAC"], ["Sitename"], ["Vendor"], ["Geoposition"], ["Uptime"], ["Seen"]]) #DATA GATEWAY DOWN SAAT ITU
    print("status length: ", len(excelStatus))
    print("mac length: ", len(excelMAC))
    print("sitename length: ", len(excelSitename))
    print("vendor length: ", len(excelVendor))
    print("Geoposition length: ", len(excelGeoposition))
    print("uptime length: ", len(excelUptime))
    print("seen length: ", len(excelSeen))
    print("Power length: ", len(excelPower))
    print("WWAN length: ", len(excelWWAN))
    print("Ethernet length: ", len(excelEthernet))
    print("GNSS length: ", len(excelMonitoring))
    print("\nIf the length is not the same for all, contact: 081319771165(WA) \n")
    #print("Power length: ", len(excelPower))
    #print("Power length: ", len(excelPower))
    #print("Power length: ", len(excelPower))
    
    
    ExcelFile = pd.DataFrame(excelData, columns = ["Status", "MAC", "Sitename", "Vendor", "Geoposition", "Uptime", "Seen", "Power", "WWAN", "Ethernet", "GNSS", "LoRa"]) #DATA GATEWAY DOWN SAAT ITU
    #ExcelFile = ExcelFile.transpose()
    
    
    print("Creating excel file now...")
    current_date_and_time = datetime.datetime.now().strftime('%H.%M.%S (%d-%m-%Y)') #ambil data jam saat itu
    current_date_and_time_string = str(current_date_and_time)   #jadikan jam menjadi tipe string
    current_date_and_time_string = current_date_and_time_string
    extension = ".xlsx" #ekstension file image nya
    filename =  current_date_and_time_string + extension  #nama save-an screenshot nya                                                                                                        
    ExcelFile.to_excel(filename, engine='xlsxwriter')
    print("Excel file has been created")
    return filename

TXTfileDelete = ""
def deleteTXTfile(txtfile):

    global TXTfileDelete
    path = 'C:/Users/t/Documents/LoRa Ultimate Automation/' + txtfile
    try:
        os.remove(path)
        TXTfileDelete = ""
        print("Successfully delete junk file")
    except:
        print("No file to be deleted")


def buatTXTfile():


    print("Creating TXT file now...")
    current_date_and_time = datetime.datetime.now().strftime('%H.%M.%S (%d-%m-%Y)') #ambil data jam saat itu
    current_date_and_time_string = str(current_date_and_time)   #jadikan jam menjadi tipe string
    current_date_and_time_string = current_date_and_time_string
    extension = ".txt" #ekstension file image nya
    filename =  current_date_and_time_string + extension  #nama save-an screenshot nya                                                                                                        
    #ExcelFile.to_excel(filename, engine='xlsxwriter')
    
    file= open(filename,"w+")

    file.write("\n\n__________________________________All Gateway Down____________________________________\n")
    """
    p = 0
    q = 0
    for p in range(len(gatewayError)):
        for q in range(Gateway):
            Hasil = cekDetailError(q, str(gatewayError[p]), "Down")
            if(Hasil == None): pass
            else: gatewayError[p] = Hasil
 
    sortedGatewayError = []
    bubble_sort(variabelWaktu, variabelNama)
    #print(variabelWaktu, variabelNama) 
    p = 0
    q = 0
    for p in range(len(variabelNama)):
        for q in range(len(gatewayError)):
            sortTrue = variabelNama[p] in gatewayError[q]
            if(sortTrue == True):
                sortedGatewayError.append(gatewayError[q])
                gatewayError[q] = "SUDAH" #ini biar gateway yang udah ke sort gak ketangkep lagii
    """                    

    p = 0
    for p in range(len(sortedGatewayErrorDecoy)):
        file.write(str(p+1) + " " + sortedGatewayErrorDecoy[p] + "\n")
    file.write("_____________________________________________________________________________________\n")

    file.write("\n\n___________Output____________\n")
    file.write("Total Gateway terpasang: " + str(Total) + "\n")
    file.write("Total Gateway warning: " + str(warning) + "\n")
    file.write("Total Gateway ok: " + str(ok) + "\n")
    file.write("Total Gateway error: " + str(error) + "\n")
    file.write("Total Power error : " + str(powerError) + "\n") #Karna kebawa data yg gaada mobile
    file.write("Total Ethernet error: " + str(ethernetError) + "\n")
    file.write("Total Mobile error: " + str(mobileError) + "\n") #Karna ada 1 gateway yg memang gaada mobile nya. mac = b0fd0b7009650000. ini kehitungnya malah ke powerError 
    
    file.write("\nNew Gateway Down: \n")   
    x = 0
    for x in range(len(gatewayDown)):
        file.write(str(x+1) + " " + gatewayDown[x] + "\n")
        
    file.write("\nNew Gateway Up: \n")
    x = 0
    for x in range(len(gatewayUp)):
        file.write(str(x+1) + " " + gatewayUp[x] + "\n")
    
    file.write("_____________________________\n")

    file.close()
    print("TXT file has been created")
    return filename


def buatFolder(file1, file2):
    #buat folder untuk men-save screenshot di C:\Users\t\Documents\LoRa Ultimate Automation
    saveDirectory = "C:/Users/t/Documents/LoRa Ultimate Automation/" + datetime.datetime.now().strftime('%d-%m-%Y') #INI PERLU DISESUAIKAN DENGAN DIRECTORY PROGRAMNYA
    if not os.path.exists(saveDirectory):
        os.mkdir(saveDirectory)
    #memindahkan hasil screenshot ke save directory
    files = [file1, file2]  
    for f in files:
        try:
            shutil.move(f, saveDirectory) 
        except WindowsError:
            pass

    #path = 'C:/Users/t/Documents/LoRa Ultimate Automation/' + file2 #lokasi txt file detail gateway error berada
    #os.remove(path)
        
        
Status = []
Sitename = []
Seen = []
Power = []
WWAN = []
Ethernet = []
Lora = []

Total = 0
ok = 0
warning = 0
error = 0
powerError = 0
powerOk = 0
ethernetError = 0
loraError = 0
mobileError = 0
gatewayIndo = []
gatewayError = []
gatewayDown = []
gatewayUp = []

w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)] 

gatewayErrorDecoy = gatewayError        
sortedGatewayErrorDecoy = []
variabelWaktuDecoy = variabelWaktu
variabelNamaDecoy = variabelNama


def tugasUtama():

    LoRa = requests.get(url,headers=headers, auth=auth, params=parametersLora)
    print("LoRa status code", LoRa.status_code)
    #jprint(LoRa.json())

    if(LoRa.status_code == 200):
        print("\nSuccessfully retrieve LoRa data from everynet\n")
    else:
        print("\nUnable to retrieve LoRa data with error code " + str(LoRa.status_code) + "\n")
    
    json = LoRa.json() #Kalo yang LoRa diganti LoRa.json() jadi jauh lebih lambat!

    global Status 
    global Sitename 
    global Seen 
    global Power 
    global WWAN 
    global Ethernet 
    global Lora 
    
    global Total 
    global ok 
    global warning 
    global error 
    global powerError 
    global powerOk 
    global ethernetError 
    global loraError 
    global mobileError 
    global gatewayIndo 
    global gatewayError 
    global gatewayDown 
    global gatewayUp 
    
    global gatewayErrorDecoy         
    global sortedGatewayErrorDecoy 
    global variabelWaktuDecoy
    global variabelNamaDecoy

    global excelStatus 
    global excelMAC 
    global excelSitename   
    global excelVendor 
    global excelGeoposition 
    global excelUptime 
    global excelSeen 
    global excelPower 
    global excelWWAN 
    global excelEthernet 
    global excelGNSS 
    global excelMonitoring 
    global excelControl 
    global excelLoRa 

    global TXTfileDelete
    #LoRa = requests.get(url,headers=headers, auth=auth, params=parametersLora)
    #print("LoRa status code", LoRa.status_code)
    #if(LoRa.status_code == 200):
    #    print("\nSuccessfully retrieve LoRa data from everynet\n")
    #else:
    #    print("\nUnable to retrieve LoRa data with error code " + str(LoRa.status_code) + "\n")
        
    #LoRa = LoRa.json() #Kalo yang LoRa diganti LoRa.json() jadi jauh lebih lambat!
    Gateway = int((json).get('total')) #seluruh Gateway yang didapat dari website everynet
    ExcelFile = buatExcel(json)
    
    x = 0
    for x in range(Gateway):
        arrGateway = (json).get('gateways')[x].get('lora_networks')
        gatewayTrue = "4" in arrGateway
        #print(gatewayTrue)
        
        #if( len((LoRa).get('gateways')[x].get('lora_networks'))  > 0 and str((LoRa).get('gateways')[x].get('lora_networks')[0]) == "4"): #Buat Lora Indonesia itu 4, opsi lain 3 tapi itu gatau gajelas
        if(gatewayTrue == True): 
            Total += 1
            gatewayIndo.append(str((json).get('gateways')[x].get('sitename')))
            """
            Pow = True
            ether = True
            mob = True
            sys = True
            gnss = True
            vpn = True
            """
            cekPower = True
            cekEther = True
            cekMobile = True
            cekLora = True
                    
            if( str((json).get('gateways')[x].get('system').get('status')) == "warning" or str((json).get('gateways')[x].get('system').get('status')) == "warning_power"): 
                warning += 1
            if( str((json).get('gateways')[x].get('system').get('status')) == "ok"): 
                ok += 1
            
            ##################### ALGORITMA PEMBUATAN FILE EXCEL OLEH WEBSITE EVERYNET!!! (PALING BERHARGA)############################
            got = 0 
            y = 0
            while y < len((json).get('gateways')[x].get('modules')): #ada 6 module, ada juga yg 5
                if( str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "power" and str((json).get('gateways')[x].get('modules')[y].get('status')) == "error" ) :
                    cekPower = False
                    got += 1
                if( str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "eth" and str((json).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    cekEther = False
                    got += 1
                if( str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "wwan" and str((json).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    cekMobile = False#print("mobile exist")
                    got += 1
                if( str( (json).get('gateways')[x].get('modules')[y].get('type') ) == "" ):
                    cekPower = False
                    got += 1
                if(y == len((json).get('gateways')[x].get('modules')) - 1):
                    #if( str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == ""):
                        #excelPower.append( str( (LoRa).get('gateways')[x].get('modules')[y].get('status')) )
                    if(got == 0): 
                        cekPower = True                   
                        cekEther = True
                        cekMobile = True
                    if(got == 1 and cekPower == False):
                        cekEther = True
                        cekMobile = True
                    if(got == 1 and cekEther == False):
                        cekPower = True
                        cekMobile = True
                    if(got == 1 and cekMobile == False):
                        cekPower = True
                        cekEther = True
                    if(got == 2 and cekPower == False and cekEther == False):
                        cekMobile = True
                    if(got == 2 and cekPower == False and cekMobile == False): 
                        cekEther = True
                    if(got == 2 and cekEther == False and cekMobile == False): 
                        cekPower = True
                    if(got == 3): pass
                y += 1
            
            if(cekPower == False): powerError += 1
            if(cekEther == False): ethernetError += 1
            if(cekMobile == False): mobileError += 1

            """
            y = 0
            while y < len((LoRa).get('gateways')[x].get('modules')): #ada 6 module, ada juga yg 5
                if( (str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == "power" ) and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    Pow = False              
                if( (str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == "eth" ) and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    ether = False
                if( (str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == "wwan" ) and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    mob = False
                if( (str( (LoRa).get('gateways')[x].get('modules')[y].get('name') ) == "VPN" ) and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    vpn = False
                if( (str( (LoRa).get('gateways')[x].get('modules')[y].get('name') ) == "GNSS" ) and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    gnss = False
                if( (str( (LoRa).get('gateways')[x].get('modules')[y].get('name') ) == "System" ) and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    sys = False  
                if( str( (LoRa).get('gateways')[x].get('modules')[y].get('type') ) == ""  and str((LoRa).get('gateways')[x].get('modules')[y].get('status')) == "error" ):
                    #Ini karena banya power error gaada type nya
                    #cekdataNotype(x) 
                    Pow = False    
                if(len((LoRa).get('gateways')[x].get('modules')) == 5 ): #ini karna ada 1 gateway yg memang gaada mobile nya.
                    mob = False
                    
                y += 1   
               
            #if(mob == False ):# and vpn == True and gnss == True and sys == True): 
            #    mobileError += 1         
            #    print("mob false")
            #if(Pow == True and ether == True and mob == True and vpn == True and gnss == True and sys == True):
                #print("All data received")
            if(Pow == False): powerError += 1
            if(ether == False): ethernetError += 1
            if(mob == False): mobileError += 1
            """

            if( str((json).get('gateways')[x].get('system').get('status')) == "error_power" or str((json).get('gateways')[x].get('system').get('status')) == "error" or str((json).get('gateways')[x].get('system').get('status')) == "error_recovery"): #Error itu ketika status error dan power error
                error += 1
                gatewayError.append( str(json.get('gateways')[x].get('sitename')) )  

            #debugGateway(x, "80029c09dbdf0000")
            
            #Hasil = cekDetailError(x, "Femto Gateway Telkom GMP", "Down")
            #if(Hasil == None): pass
            #else: print(Hasil)
            
            #UNTUK DEBUGGING POWER, ETHERNET, MOBILE ERROR!!!
            #if( str((LoRa).get('gateways')[x].get('mac')) == "80029c1af2fd0000" ): 
            #    jprint((LoRa).get('gateways')[x].get('modules'))
            
            #BUAT DEBUG AVAILABILITY DARI SELURUH MODULES
            #print(x, Pow, mob, ether, vpn, gnss, sys) 
            
            #MIRIP DENGAN FUNGSI DEBUG POWER< ETHERNET< MOBILE
            #debugGateway(x, "b0fd0b7009650000")

            #BUAT CEK KEY DALAM JSON
            #nonamePower = json.loads( json.dumps((LoRa).get('gateways')[x].get('modules')[y]) ) #dump buat ubah dict jadi string, karna json.load perlu input string
            #current = "current" in nonamePower
            #voltage = "voltage" in nonamePower
            #if(current == False and voltage == False):
            #    print(x,y)
            #    y += 1
            #if(current == True and voltage == True):
            #    powerOk += 1
            #    break
                
    dataset = pd.DataFrame(gatewayError, columns = ["Nama Gateway Error"]) #DATA GATEWAY DOWN SAAT ITU    

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
                    
        #Masukkan Detail Error           
        p = 0
        q = 0
        for p in range(len(gatewayDown)):
            for q in range(Gateway):
                
                Hasil = cekDetailError(json, q, str(gatewayDown[p]) , "Down")         
                if(Hasil == None): pass
                else: 
                    gatewayDown[p] = Hasil

                  

        #Masukkan Detail Up
        p = 0
        q = 0
        for p in range(len(gatewayUp)):
            for q in range(Gateway):
                Hasil = cekDetailError(json, q, str(gatewayUp[p]), "Up")
                if(Hasil == None): pass
                else: gatewayUp[p] = Hasil               
                    
                    
                    
        
        
        print("\n\n__________________________________All Gateway Down____________________________________")
        p = 0
        q = 0
        for p in range(len(gatewayError)):
            for q in range(Gateway):
                Hasil = cekDetailError(json, q, str(gatewayError[p]), "Down")
                if(Hasil == None): pass
                else: gatewayError[p] = Hasil
        
            #PROGRAM SORTING ADA DIBAWAH INI#
        gatewayErrorDecoy = gatewayError        
        sortedGatewayErrorDecoy = []
        variabelWaktuDecoy = variabelWaktu
        variabelNamaDecoy = variabelNama
        bubble_sort(variabelWaktuDecoy, variabelNamaDecoy)
        p = 0
        q = 0
        for p in range(len(variabelNamaDecoy)):
            for q in range(len(gatewayErrorDecoy)):
                SortTrue = variabelNamaDecoy[p] in gatewayErrorDecoy[q]
                if(SortTrue == True):
                    sortedGatewayErrorDecoy.append(gatewayErrorDecoy[q])
                    gatewayErrorDecoy[q] = "SUDAH" #ini biar gateway yang udah ke sort gak ketangkep lagii        
        
        
        p = 0
        for p in range(len(sortedGatewayErrorDecoy)):
            print("-" + sortedGatewayErrorDecoy[p])
        print("_____________________________________________________________________________________")

        """
        print("\n\n__________________Down Time > 3 days__________________")
        p = 0
        for p in range(len(tigaHariKeatas)):
            print("-" + tigaHariKeatas[p])
        print("________________________________________________________")

        print("\n\n______________1 days < Down Time < 3 days_____________")
        p = 0
        for p in range(len(satuHariKeatas)):
            print("-" + satuHariKeatas[p])
        print("________________________________________________________")

        print("\n\n_________________Down Time < 1 days___________________")
        p = 0
        for p in range(len(satuHariKebawah)):
            print("-" + satuHariKebawah[p])
        print("________________________________________________________")
        """
        
        
        #print(data)
        print("\n\n___________Output____________")
        print("Total GW. Terpasang     : ", Total)
        print("Total GW. Warning       : ", warning)
        print("Total GW. Normal        : ", ok)
        print("Total GW. Error         : ", error)
        print("Total GW. Power Error   : ", powerError) #Karna kebawa data yg gaada mobile
        print("Total GW. Ethernet Error: ", ethernetError)
        print("Total GW. Bachkaul Error: ", mobileError) #Karna ada 1 gateway yg memang gaada mobile nya. mac = b0fd0b7009650000. ini kehitungnya malah ke powerError 
        
        detailOutput = ''.join(("\n\n        *Output*\n",
                              "Total GW. Terpasang     : " + str(Total) + "\n",
                              "Total GW. Warning       : " + str(warning) + "\n",
                              "Total GW. Normal        : " + str(ok) + "\n",
                              "Total GW. Error         : " + str(error) + "\n",
                              "Total GW. Power Error   : " + str(powerError) + "\n",
                              "Total GW. Ethernet Error: " + str(ethernetError) + "\n",
                              "Total GW. Bachkaul Error: " + str(mobileError) + "\n\n"))
        

        
        print("\nNew Gateway Down: ")   
        x = 0
        for x in range(len(gatewayDown)):
            print(gatewayDown[x])
            
        print("\nNew Gateway Up: ")
        x = 0
        for x in range(len(gatewayUp)):
            print(gatewayUp[x])
        
        print("_____________________________")

        dataset.to_excel("dataset.xlsx")
        print("\nDataset has been updated")
        #print("Thank you for using this program :)")
        
        messageDown = '\n'.join(gatewayDown) #Buat ngubah list jadi string dengan separator \n
        messageUp = '\n'.join(gatewayUp) #Buat ngubah list jadi string dengan separator \n

        TXTfile = buatTXTfile()  #Ngedapetin Nama TXTfile
        laporanPukul = datetime.datetime.now().strftime('%H.%M.%S (%d-%m-%Y)') #Buat Judul Laporan Telegram  
        
        #DIBAWAH INI KODE BUAT KIRIM KE TELEGRAM
        botName = "Mr. LoRa"
        botUsername = "Mr_LoRa_Bot"
        client = TelegramClient('session', api_id, api_hash)
        #client.connect()
        client.start() #ini harus pake start. connect bisa kalo untuk akun sendiri.
        client.send_message(botUsername, 'Laporan LoRa pukul ' + laporanPukul + detailOutput + "New Gateway Down: \n" + messageDown + "\n\n" + "New Gateway Up: \n" + messageUp )
        client.send_file(botUsername, 'C:/Users/t/Documents/LoRa Ultimate Automation/' + TXTfile) #INI PERLU DISESUAIKAN DENGAN DIRECTORY PROGRAMNYA

        #Send to group
        message = 'Laporan pukul ' + laporanPukul + detailOutput + "New Gateway Down: \n" + messageDown + "\n\n" + "New Gateway Up: \n" + messageUp
        send_message(groupid, token, message)

        path = 'C:/Users/t/Documents/LoRa Ultimate Automation/' + TXTfile #lokasi txt file detail gateway error berada
        files = {'document':open(path,'rb')} #membuka sebuah dokumen dari path
        resp = requests.post('https://api.telegram.org/bot1665551618:AAFvpiCLP19vYNPVez0-wlNFdcEe8HlK2Jw/sendDocument?chat_id=-1001249682496&caption=All_Gateway_Down_Detail_at: {}'.format(laporanPukul), files = files)

        client.disconnect()
        print("\nMessage successfully sent to telegram")
        buatFolder(ExcelFile, TXTfile) #pindahkan file excel dan file txt ke folder sesuai tanggal hari ini

        TXTfileDelete = TXTfile
        #os.remove(path)
        
        Status = []
        Sitename = []
        Seen = []
        Power = []
        WWAN = []
        Ethernet = []
        Lora = []
        
        Total = 0
        ok = 0
        warning = 0
        error = 0
        powerError = 0
        powerOk = 0
        ethernetError = 0
        loraError = 0
        mobileError = 0
        gatewayIndo = []
        gatewayError = []
        gatewayDown = []
        gatewayUp = []
        
        gatewayErrorDecoy = []       
        sortedGatewayErrorDecoy = []
        variabelWaktuDecoy = []
        variabelNamaDecoy = []

        excelStatus = []
        excelMAC = []
        excelSitename = []   
        excelVendor = []
        excelGeoposition = []
        excelUptime = []
        excelSeen = []
        excelPower = []
        excelWWAN = []
        excelEthernet = []
        excelGNSS = []
        excelMonitoring = []
        excelControl = []
        excelLoRa = []

        print("TXT file will be deleted:")
        print(TXTfileDelete)
        
    else:
        print("Dataset is not yet created")
        print("Creating Dataset now..")
        dataset.to_excel("dataset.xlsx")
        print("Dataset has been created")
        print("You can run again this program to get the output")
    
    
    
    
##################################DOKUMENTASI ADA DIBAWAH INI############################
#def some_job():
#while(1):
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


"""#                 DIBAWAH INI BUAT AMBIL DATA JSON LORA
LoRa = requests.get(url,headers=headers, auth=auth, params=parametersLora)
print("LoRa status code", LoRa.status_code)
#jprint(LoRa.json())

if(LoRa.status_code == 200):
    print("\nSuccessfully retrieve LoRa data from everynet\n")
else:
    print("\nUnable to retrieve LoRa data with error code " + str(LoRa.status_code) + "\n")
"""

#LoRa = LoRa.json()
#LoRa = LoRa.get('gateways')
#jprint(LoRa.json())


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
powerError = 0
powerOk = 0
ethernetError = 0
loraError = 0
mobileError = 0
gatewayIndo = []
gatewayError = []
gatewayDown = []
gatewayUp = []

w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)] 


#print(Gateway)
#LoraNetwork = len((LoRa.json()).get('gateways')[146].get('lora_networks'))
#LoRa = LoRa.json() #Kalo yang LoRa diganti LoRa.json() jadi jauh lebih lambat!
#Modules = int(len((LoRa).get('gateways')[631].get('modules')))
#Gateway = int((LoRa).get('total')) #seluruh Gateway yang didapat dari website everynet--------------------------------dipakai
#nonamePower = json.loads(LoRa)


#ExcelFile = buatExcel(LoRa)#----------------------------------dipakai

       
dataset = pd.DataFrame(gatewayError, columns = ["Nama Gateway Error"]) #DATA GATEWAY DOWN SAAT ITU
#print("\n Nama Gateway error: ")
#print(dataset)


print("\n\nLora Automation has been started\n")
#every minute at :00 artinya setiap menit jalan saat detiknya mencapai XX:00
schedule.every().hour.at(":03").do(lambda: tugasUtama())
schedule.every().hour.at(":30").do(lambda: reLogin())
schedule.every().hour.at(":10").do(lambda: reLogin())
schedule.every().hour.at(":20").do(lambda: reLogin())
schedule.every().hour.at(":40").do(lambda: reLogin())
schedule.every().hour.at(":50").do(lambda: reLogin())
schedule.every().hour.at(":15").do(lambda: deleteTXTfile(TXTfileDelete))
#schedule.every().hour.at(":33").do(lambda: reLogin())
#schedule.every().hour.at(":20").do(lambda: tugasUtama())

while True:
    schedule.run_pending()
    time.sleep(1)


    