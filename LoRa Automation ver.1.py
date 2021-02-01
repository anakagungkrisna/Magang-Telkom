
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile

excel_file1 = 'Total.xls'
excel_file2 = 'Total2.xls'
sheetname = 'Sheet1' #nama sheet yang ingin dibaca
index_col = 0 #gatau ini buat apa. baca lagi

offset1 = 0 #total data yang lebih banyak
offset2 = 0 #total data yang lebih dikit
offsetPembeda = 0 #total data yang berbeda
perbandingan = pd.DataFrame([[None, None, None]], columns = ["Pembeda", "Down","Up"]) #dataframe hasil gateway up dan down
baruTerpasang = pd.DataFrame([None], columns = ["Baru Terpasang"]) #dataframe gateway baru terpasang
#print(perbandingan) #cek kondisi awal perbandingan





parse_cols = 0
errorTotal = 0
warningTotal = 0
powerError = 0
totalWWAN = 0
totalEther = 0
totalLoRa = 0
down = 0
up = 0


#data = pd.read_excel(excel_file1, sheetname,index_col)
#print(data.head())
#print(data.shape)
#print(data.tail())
#print(data.describe())

#buat baca Total
data1 = pd.read_excel(excel_file1, index_col=None, na_values=['NA'], usecols = "A,C,G,H,I,J,L,N")
data1_subset = data1[['Status','Sitename']]
#buat baca Total2
data2 = pd.read_excel(excel_file2, index_col=None,na_values=['NA'], usecols = "A,C,G,H,I,J,L,N")
data2_subset = data2[['Status','Sitename']]

#ini buat nentuin jumlah pembacaannya
#data.columns = ['MAC', 'Vendor', 'Geoposition', 'Seen', 'GNSS', 'Monitoring', 'Control',]
print("\n\n--------------Total-------------")
print(data1_subset.head(50))
print(len(data1_subset))
print(data2_subset.head(50))
print(len(data2_subset))
print("--------------------------------")
print("")



#code dibawah ini buat dataframe baru berisi semua gateway yang baru terpasang
#caranya dengan membandingkan Total2.xls dengan Total.xls
baruTerpasang = pd.concat([data1_subset['Sitename'],data2_subset['Sitename']]).drop_duplicates(keep=False)
#hasil si pembeda perlu di reset indexnya jadi mulai dari 0 lagi
baruTerpasang = baruTerpasang.reset_index() #buat kolom index, reset index pembeda keseluruhan
offsetbaruTerpasang = len(baruTerpasang)
#buat ngeprint seluruh isi dataframe  
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(perbandingan)  





##buat mencatat error dari Total.xls##
error1 = pd.DataFrame(data1['Status']) #membuat dataframe baru
error1 = error1['Status'].str.contains(r'error',na = True) #ubah isi dataframe, kalo error True, else False
error1new = pd.DataFrame([np.nan], columns = ["error data 1"]) #membuat dataframe baru

for x in range(len(error1)):
    if(error1.loc[x] == True):
        error1new.loc[x] = data1_subset.loc[x, 'Sitename']
 
error1new = error1new.reset_index() #Reset index
print("\t-------error pada data 1-------")
print(error1new.head(10))
print("Total error:", len(error1new))
print("\t-------------------------------")
print("\n\n")
####################################


##buat mencatat error dari Total2.xls##
error2 = pd.DataFrame(data2['Status'])
error2 = error2['Status'].str.contains(r'error',na = True)
error2new = pd.DataFrame([np.nan], columns = ["error data 2"])

for x in range(len(error2)):
    if(error2.loc[x] == True):
        error2new.loc[x] = data2_subset.loc[x, 'Sitename']

error2new = error2new.reset_index() #Reset index   
print("\t-------error pada data 2-------")
print(error2new.head(10))
print("Total error:", len(error2new))
print("\t-------------------------------")
print("\n\n")
####################################



#Loop ini buat dataframe baru berisi semua gateway yang membedakan error pada Total.xls dan Total2.xls
errorBanding = pd.concat([error1new['error data 1'],error2new['error data 2']]).drop_duplicates(keep=False)
errorBanding = errorBanding.reset_index() #buat kolom index, reset index pembeda keseluruhan
x = 0
for x in range(len(errorBanding)):
    perbandingan.loc[x,'Pembeda'] = errorBanding.loc[x,0]      
#buat ngeprint seluruh isi dataframe  
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(perbandingan)  
##############################



##Buat mencatat gateway yang down##
x = 0
y = 0
i = 0
for x in range(len(perbandingan)):
    for y in range(len(error1new)):
        #print("hehe")
        if( perbandingan.loc[x,'Pembeda'] == error1new.loc[y,'error data 1'] ):
            #print("MANTAPS")
            perbandingan.loc[i,"Up"] = error1new.loc[y,'error data 1']
            i += 1
            break
        else: 
            continue
##Buat mencatat gateway yang up##
x = 0
y = 0   
j = 0       
for x in range(len(perbandingan)):
    for y in range(len(error2new)):
        #print("hehe")
        if( perbandingan.loc[x,'Pembeda'] == error2new.loc[y,'error data 2']) :
            perbandingan.loc[j,"Down"] = error2new.loc[y,'error data 2']
            j += 1
        else: 
            continue

#ini buat display error pembeda, gateway down, gateway up
print("\t\t-----Hasil Perbandingan Error-----\n")
print(perbandingan.head(20))
print("\nTotal perbandingan:", len(perbandingan)) 
print("\t\t----------------------------------")
print("\n\n")
##################################


##Menulis detail gateway yang down##
if(perbandingan.loc[0,'Down'] == None):
    down = -1
    print("\t\t-------Detail Gateway Down-------\n")
    print("There is no Gateway Down")
    print("\nTotal Gateway Down:", 0) 
    print("\t\t----------------------------------")
    print("\n\n") 
else:
    detailDown = pd.DataFrame([[None, None, None, None, None, None]], columns = ["Gateway Down", "Power", "Mobile","Ethernet","Lora", "Waktu"]) #dataframe buat detail gateway down
    x = 0
    y = 0   
    j = 0       
    for x in range(len(perbandingan)):
        for y in range(len(data2)):
            if( perbandingan.loc[x,'Down'] == data2.loc[y,'Sitename']) :
                detailDown.loc[j,"Gateway Down"] = data2.loc[y,'Sitename']
                detailDown.loc[j,"Power"] = data2.loc[y,'Power']
                detailDown.loc[j,"Mobile"] = data2.loc[y,'WWAN']
                detailDown.loc[j,"Ethernet"] = data2.loc[y,'Ethernet']
                detailDown.loc[j,"Lora"] = data2.loc[y,'LoRa']
                detailDown.loc[j,"Waktu"] = data2.loc[y,'Seen']
                j += 1
            else: 
                continue
    detailDown.dropna(inplace = True)
    new = detailDown["Waktu"].str.split(" ", n = 1, expand = True)
    detailDown["Tanggal"] = new[0]
    detailDown["Jam"] = new[1]
    detailDown.drop(columns = ["Waktu"], inplace = True)

    #detailDown = detailDown['Lora'].str.contains(r'error',na = True)            
    print("\t\t-------Detail Gateway Down-------\n")
    print(detailDown.head(20))
    print("\nTotal Gateway Down:", len(detailDown)) 
    print("\t\t----------------------------------")
    print("\n\n")                       
###################################


##Menulis detail gateway yang up##
if(perbandingan.loc[0,'Up'] == None):
    up = -1
    print("\t\t-------Detail Gateway Up-------\n")
    print("There is no Gateway Up")
    print("\nTotal Gateway Up:", 0) 
    print("\t\t----------------------------------")
    print("\n\n")  
else:
    detailUp = pd.DataFrame([[None, None]], columns = ["Gateway Up", "Waktu"]) #dataframe buat detail gateway up
    x = 0
    y = 0   
    j = 0       
    for x in range(len(perbandingan)):
        for y in range(len(data2)):
            if( perbandingan.loc[x,'Up'] == data2.loc[y,'Sitename']) :
                detailUp.loc[j,"Gateway Up"] = data2.loc[y,'Sitename']
                detailUp.loc[j,"Waktu"] = data2.loc[y,'Seen']
                j += 1
            else: 
                continue
    detailUp.dropna(inplace = True)
    new = detailUp["Waktu"].str.split(" ", n = 1, expand = True)
    detailUp["Tanggal"] = new[0]
    detailUp["Jam"] = new[1]
    detailUp.drop(columns = ["Waktu"], inplace = True)

    #detailDown = detailDown['Lora'].str.contains(r'error',na = True)            
    print("\t\t-------Detail Gateway Up-------\n")
    print(detailUp.head(20))
    print("\nTotal Gateway Up:", len(detailUp)) 
    print("\t\t----------------------------------")
    print("\n\n")                       
##################################





#print(perbandingan.head(20))
#print(perbandingan.shape)
print("----------Baru Terpasang---------")
print(baruTerpasang.head(20))
print("Total baru terpasang:", offsetbaruTerpasang)
print("----------------------------------")
print("")
#print(data2_subset.head())

#ini buat sum power error
test = pd.DataFrame(data2['Power']) #buat ambil dari data2 kolom 'Power'
test = test.replace('ok',np.nan) #buat ganti 'ok' jadi yang dari numpy

errorPower = test['Power'].str.contains(r'error',na = True)
_power = test['Power'].str.contains(r'-',na = True)

#print(test) #ini dataframe untuk kolom WWAN
#print(errorPower) #ini dataframe ketika sudah di filter
#########################


#ini buat sum WWAN error
WWAN = pd.DataFrame(data2['WWAN'])
WWANerror = WWAN['WWAN'].str.contains(r'error',na = True)

#print(WWAN) #ini dataframe untuk kolom WWAN
#print(WWANerror) #ini dataframe ketika sudah di filter
########################


#ini buat Ethernet error
Ether = pd.DataFrame(data2['Ethernet'])
EtherError = Ether['Ethernet'].str.contains(r'error',na = True)

#print(Ether) #ini dataframe untuk kolom WWAN
#print(EtherError) #ini dataframe ketika sudah di filter
##########################


#ini buat LoRa error
LoRa = pd.DataFrame(data2['LoRa'])
LoRaError = LoRa['LoRa'].str.contains(r'error',na = True)

#print(LoRa)
#print(LoRaError)
####################








#penambahan setiap parameter total
for x in range(len(data2)):
    #buat total error
    if(data2.loc[x,'Status'] == 'ok'): 
        errorTotal += 1
    #buat total warning
    if(data2.loc[x,'Status'] == 'warning' or data2.loc[x,'Status'] == 'warning_power'):
        warningTotal += 1
    #buat total power error
    if(errorPower.loc[x] == True or _power.loc[x] == True):
        powerError += 1
    #buat total WWAN error
    if(WWANerror.loc[x] == True):
        totalWWAN += 1
    #buat total Ethernet error
    if(EtherError.loc[x] == True):
        totalEther += 1
    if(LoRaError.loc[x] == True):
        totalLoRa += 1
        


#print hasil kalkulasi
print("\n\n\n\n")
print("*****************Output*********************")
print("Total:",len(data2))
print("error:",errorTotal)
print("warning:",warningTotal)
print("Power error:",powerError)
print("WWAN error:",totalWWAN)
print("Ethernet error:",totalEther)
print("LoRa error:",totalLoRa)



##Menulis catatan##
if(down == 0):
    boolPower = detailDown['Power'].str.contains(r'error', na=True)
    boolPower2 = detailDown['Power'].str.contains(r'-', na=True)
    boolMobile = detailDown['Mobile'].str.contains(r'error', na=True)
    boolEthernet = detailDown['Ethernet'].str.contains(r'error', na=True)
    boolLora = detailDown['Lora'].str.contains(r'error', na=True)

"""
print("____________________________")
print(boolPower)
print(boolMobile)
print(boolEthernet)
print(boolLora)
print("____________________________")
"""

power = ""
mobile = ""
ethernet = ""
lora = ""
x = 0
y = 0

print("\nCatatan:")
print("Gateway Lora Down:")
if(down == -1):
    print("No Gateway Down")
else:
    for x in range(len(detailDown)):
        if(boolPower.loc[x] == True):
            power = "Power,"
        else:
            power = ""
        if(boolMobile.loc[x] == True):
            mobile = "Mobile,"
        else:
            mobile = ""
        if(boolEthernet.loc[x] == True):
            ethernet = "Ethernet,"
        else:
            ethernet = ""
        if(boolLora.loc[x] == True):
            lora = "Lora"
        else:
            lora = ""       
        print("- ",detailDown.loc[x,'Gateway Down'], " down ", "(", power, mobile, ethernet, lora," error", ")", " pukul ", detailDown.loc[x, 'Jam']," WIB ", "(",detailDown.loc[x, 'Tanggal'], ")",sep='')      
print("") 
print("Gateway Lora Up:")
if(up == -1):
    print("No gateway Up")
else: 
    for y in range(len(detailUp)):
        print("- ",detailUp.loc[y,'Gateway Up'], " Up pukul ",detailUp.loc[y,'Jam'], " (", detailUp.loc[y,'Tanggal'], ")", sep='')
###############################



input("\nPress Enter to continue...")

#data2 = data2.replace('error',np.nan)



#print("\n")







"""
df = pd.DataFrame({'a': ['NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN'],
 'b': ['BABA UN EQUITY', '2018', '2017', '2016', 'NAN', '700 HK EQUITY', '2018', '2017', '2016', 'NAN']})

# Make sure that all NaN values are `np.nan` not `'NAN'` (strings)
df = df.replace('NAN', np.nan)
mask = df['b'].str.contains(r'EQUITY', na=True)
df.loc[mask, 'a'] = df['b']
df['a'] = df['a'].ffill()
df.loc[mask, 'a'] = np.nan
"""
    
#print(df)
        