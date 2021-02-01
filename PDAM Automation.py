
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



#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pdam.antares.id/auth/login')

username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("pdamsemarang")
password.send_keys("antares2020")

#driver.find_element(By.XPATH, '//button[text()="Sign In"]')
#driver.find_elements(By.XPATH, '//button')

#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//input[@class='btn btn-primary btn-user btn-block' and @type='submit']")[0]
time.sleep(1)
python_button.click()

active_device = driver.find_elements_by_xpath("//a[@class='nav-link' and @href='/dashboard/monitoringlist']")[0]
time.sleep(1)
active_device.click()

#ambil screenshot PDAM meter
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S')
current_date_and_time_string = str(current_date_and_time)
extension = ".png"
file_pdam =  current_date_and_time_string + " PDAM" + extension  
                                                                                                            
driver.find_element_by_tag_name('body').screenshot(file_pdam)

#dibawah ini cari xpath nya harus sesuai, kaloga bisa dia gak ada element atau unable to locate element atau apalah
Device1 = driver.find_element_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd']//td[@style='white-space : nowrap;']//span[@class='badge badge-success text-white']").text
waktuDevice1 = driver.find_element_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd']//td//p").text
DeviceName1 = driver.find_element_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd'][2]//td[1]").text #INDEX MULAI DARI 1!!!
DeviceEUI1 = driver.find_element_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd']//td[2]").text #INDEX MULAI DARI 1!!!
DeviceOrganization1 = driver.find_element_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd']//td[3]").text #INDEX MULAI DARI 1!!!
DeviceHardwareType1 = driver.find_element_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd']//td[4]").text #INDEX MULAI DARI 1!!!

#all_spans = driver.find_elements_by_xpath("//tbody[@id='data-device']//tr[@id='table-data' and @class='odd']//td")
#for span in all_spans:
#    print(span.text)
    
print("Device name: ", DeviceName1)
print("Device EUI: ", DeviceEUI1)
print("Device Organization: ", DeviceOrganization1)
print("Device hardware type: ", DeviceHardwareType1)
print("Time stamp: ", waktuDevice1)
