from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.firefox.options import Options
import os
from datetime import datetime
import shutil, os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select




#parameter buat ambil screenshot!
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)

################Membuka website PJU Ciamis##################
#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pju.telkomiot.com/login')

username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("pjuciamis")
password.send_keys("pjucms")

#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//button[@class='btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20' and @type='submit']")[0]
time.sleep(1.5) #perlu karna website pju ada delay dulu sebelum responsif
python_button.click()

time.sleep(1.5)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S')
current_date_and_time_string = str(current_date_and_time)
extension = ".png"
file_ciamis =  current_date_and_time_string + " Ciamis" + extension                                                                                                          
driver.find_element_by_tag_name('body').screenshot(file_ciamis)

Ciamis1 = driver.find_element_by_xpath("//table[@class='jvt table table-striped bulk_action row-clickable m-b-0 dataTable no-footer' and @style='width:100%;font-size:10px;']//tbody//tr//td[1]").text #INDEX MULAI DARI 1!!!
print(Ciamis1)

driver.quit() #close firefoxnya
#driver.quit()
#driver.quit()
#driver.quit()
#driver.quit()
############################################

#Membuka website PJU Pangandaran
#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pju.telkomiot.com/login')

username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("pjupangandaran")
password.send_keys("qaz123")

#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//button[@class='btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20' and @type='submit']")[0]
time.sleep(1.5) #perlu karna website pju ada delay dulu sebelum responsif
python_button.click()

time.sleep(1.5)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S') #ambil data jam saat itu
current_date_and_time_string = str(current_date_and_time)   #jadikan jam menjadi tipe string
extension = ".png" #ekstension file image nya
file_pangandaran =  current_date_and_time_string + " Pangandaran" + extension  #nama save-an screenshot nya                                                                                                        
driver.find_element_by_tag_name('body').screenshot(file_pangandaran) #buat ambil screenshot nya

driver.quit() #close firefoxnya


#Membuka website PJU Jayapura
#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pju.telkomiot.com/login')

username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("admin")
password.send_keys("qaz123")

#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//button[@class='btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20' and @type='submit']")[0]
time.sleep(1.5) #perlu karna website pju ada delay dulu sebelum responsif
python_button.click()

time.sleep(1.5)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S') #ambil data jam saat itu
current_date_and_time_string = str(current_date_and_time)   #jadikan jam menjadi tipe string
extension = ".png" #ekstension file image nya
file_jayapura =  current_date_and_time_string + " Jayapura" + extension  #nama save-an screenshot nya                                                                                                        
driver.find_element_by_tag_name('body').screenshot(file_jayapura) #buat ambil screenshot nya

driver.quit() #close firefoxnya


#Membuka website PJU Tasikmalaya
#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pju.telkomiot.com/login')

username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("pjutasikmalaya")
password.send_keys("qaz123")

#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//button[@class='btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20' and @type='submit']")[0]
time.sleep(1.5) #perlu karna website pju ada delay dulu sebelum responsif
python_button.click()

time.sleep(1.5)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S') #ambil data jam saat itu
current_date_and_time_string = str(current_date_and_time)   #jadikan jam menjadi tipe string
extension = ".png" #ekstension file image nya
file_tasikmalaya =  current_date_and_time_string + " Tasikmalaya" + extension  #nama save-an screenshot nya                                                                                                        
driver.find_element_by_tag_name('body').screenshot(file_tasikmalaya) #buat ambil screenshot nya

driver.quit() #close firefoxnya


#Membuka website PJU Garut
#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pju.telkomiot.com/login')

username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("pjugarut")
password.send_keys("pjugrt")

#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//button[@class='btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20' and @type='submit']")[0]
time.sleep(1.5) #perlu karna website pju ada delay dulu sebelum responsif
python_button.click()

time.sleep(1.5)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S') #ambil data jam saat itu
current_date_and_time_string = str(current_date_and_time)   #jadikan jam menjadi tipe string
extension = ".png" #ekstension file image nya
file_garut =  current_date_and_time_string + " Garut" + extension  #nama save-an screenshot nya                                                                                                        
driver.find_element_by_tag_name('body').screenshot(file_garut) #buat ambil screenshot nya

driver.quit() #close firefoxnya



#buat folder untuk men-save screenshot
saveDirectory = "D:/Krisna/Magang Telkom/Research/Ultimate Automation/" + datetime.now().strftime('%d-%m-%Y') #%H-%M-%S')
if not os.path.exists(saveDirectory):
    os.mkdir(saveDirectory)
#memindahkan hasil screenshot ke save directory
files = [file_ciamis, file_garut, file_jayapura, file_pangandaran, file_tasikmalaya]  
for f in files:
    shutil.move(f, saveDirectory) 
driver.quit()


