import glob
from datetime import datetime
import matplotlib.pyplot as plt
import os


totalTerpasang = []
totalWarning = []
totalOk = []
totalError = []
totalPowerError = []
totalEthernetError = []
totalMobileError = []

#Mengambil semua folder dengan format nama %d-%m-%Y dalam directory rootdir dan disortir
captureFile = []
rootdir = os.getcwd() #Directory tempat berada si graph making.py nya
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        captureFile.append(file)
captureFile.sort(key = lambda date: datetime.strptime(date, '%d-%m-%Y'))
print(captureFile)
        
xAxis = [] #diperlukan untuk variable x pada plotting graph
for everyFile in captureFile:

    #Membuka folder sesuai tanggal, mengambil semua nama .txt file
    dateNow = datetime.today().strftime('%d-%m-%Y')#ambil tanggal sekarang
    #globFormat = dateNow + '/*.txt'
    globFormat = everyFile + '/*.txt' #contoh '06-04-2021/*.txt'
    txt_files = glob.glob(globFormat) #ambil semua file .txt pada directory everyFile saat itu
    txtFiles = []
    for fileName in txt_files:
        dibuang,diambil = fileName.split("\\")
        txtFiles.append(diambil)
        xAxis.append(diambil)
    print(txtFiles)



    #Looping ke semua .txt file sesuai nama dalam predefined directory, ambil nilai totalnya saja
    directory = everyFile + '/'
    #directory = "06-04-2021/"
    for txtFile in txtFiles:
        lines = []
        with open(directory + txtFile) as f:
            lines = f.readlines()

        count = 0
        for line in lines:
            if "Total Gateway terpasang" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalTerpasang.append(int(word))
                        
            if "Total Gateway warning" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalWarning.append(int(word))
                        
            if "Total Gateway ok" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalOk.append(int(word))
            
            if "Total Gateway error" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalError.append(int(word))
                       
            if "Total Power error" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalPowerError.append(int(word))
                        
            if "Total Ethernet error" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalEthernetError.append(int(word))
                        
            if "Total Mobile error" in line:
                count += 1
                print(f'line {count}: {line}') 
                for word in line.split():
                    if word.isdigit():
                        totalMobileError.append(int(word))

            
print(totalTerpasang)
print(totalWarning)
print(totalOk)
print(totalError)
print(totalPowerError)
print(totalEthernetError)
print(totalMobileError)

x_axis = [s.strip('.txt') for s in xAxis] #removing .txt in the end of the x_axis variable     
y_axis1 = totalTerpasang
y_axis2 = totalWarning
y_axis3 = totalOk
y_axis4 = totalError
y_axis5 = totalPowerError
y_axis6 = totalEthernetError
y_axis7 = totalMobileError

plt.plot(x_axis, y_axis1, markersize=4, marker='o', linestyle='dashed', label = "total gateway terpasang" )
plt.plot(x_axis, y_axis2, markersize=4, marker='o', label = "total gateway warning" )
plt.plot(x_axis, y_axis3, markersize=4, marker='o', linestyle='dashed', label = "total gateway ok" )
plt.plot(x_axis, y_axis4, markersize=4, marker='o', label = "total gateway error" )
plt.plot(x_axis, y_axis5, markersize=4, marker='o', label = "total gateway pow error" )
plt.plot(x_axis, y_axis6, markersize=4, marker='o', linestyle='dashed', label = "total gateway eth error" )
plt.plot(x_axis, y_axis7, markersize=4, marker='o', linestyle='dashed', label = "total gateway mob error" )

plt.xticks(rotation = 80, fontsize = 8)
plt.xlabel('timestamp') # naming the x axis
plt.ylabel('jumlah gateway') # naming the y axis
plt.title('Grafik Status Gateway') # giving a title to my graph
plt.legend()
plt.show()# function to show the plot


#Source for how to get specific data from all .txt file in a folder with a name of todays date
#https://www.kite.com/python/answers/how-to-extract-integers-from-a-string-in-python
#https://www.afternerd.com/blog/python-string-contains/
#https://www.pythontutorial.net/python-basics/python-read-text-file/
#https://stackoverflow.com/questions/50848764/split-string-into-two-parts-only
#https://stackoverflow.com/questions/35672809/how-to-read-a-list-of-txt-files-in-a-folder-in-python/35674591


#source how to plot a graph python
#https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/














