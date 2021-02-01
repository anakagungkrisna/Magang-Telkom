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


#firefoxDriver = "D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe"
driver = webdriver.Firefox(executable_path=r'D:\Krisna\Magang Telkom\Research\Ultimate Automation\geckodriver.exe')  # Or Chrome(), or Ie(), or Opera()
driver.get('https://pju.telkomiot.com/login')



username = driver.find_element_by_name("username") #perlu diinspect by nya dengan cara inspect element
password = driver.find_element_by_name("password")

username.send_keys("pjuciamis")
password.send_keys("pjucms")


#driver.find_element(By.XPATH, '//button[text()="Sign In"]')
#driver.find_elements(By.XPATH, '//button')


#driver.find_element_by_class_name("btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20").click()
#ActionChains(driver).click("Sign In").perform()
python_button = driver.find_elements_by_xpath("//button[@class='btn btn-primary btn-md btn-block waves-effect waves-light text-center m-b-20' and @type='submit']")[0]
time.sleep(1.5)
python_button.click()



time.sleep(1.5)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment  

current_date_and_time = datetime.now().strftime('%H.%M.%S')
current_date_and_time_string = str(current_date_and_time)
extension = ".png"
file_ciamis =  current_date_and_time_string + " Ciamis" + extension  
                                                                                                            
driver.find_element_by_tag_name('body').screenshot(file_ciamis)


driver.quit() #close firefoxnya



#buat folder untuk men-save screenshot
saveDirectory = "D:/Krisna/Magang Telkom/Research/Ultimate Automation/" + datetime.now().strftime('%d-%m-%Y') #%H-%M-%S')
if not os.path.exists(saveDirectory):
    os.mkdir(saveDirectory)
#memindahkan hasil screenshot ke save directory
files = [file_ciamis]  
for f in files:
    shutil.move(f, saveDirectory) 
driver.quit()


