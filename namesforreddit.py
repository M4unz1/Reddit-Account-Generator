from cgitb import reset
from os.path import dirname
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import string
import secrets
import os
import sys
from twocaptcha import TwoCaptcha

api_key= 'API_KEY'
url = 'https://www.reddit.com/register/'

driver = webdriver.Chrome(ChromeDriverManager().install()) # USES CHROMEDRIVERMANAGER TO AUTO UPDATE CHROMEDRIVER


solver = TwoCaptcha(api_key)
# GENERATE PASSWORD

alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(16))
# PASSWORD GENERATION FINISHED

# NAME GENERATION
driver.get('https://en.wikipedia.org/wiki/Special:Random')
temp = driver.find_element(By.CLASS_NAME, "firstHeading").text
for char in string.punctuation:
    temp = temp.replace(char, '') #REMOVES ALL PUNCTUATION
for char in string.digits:
    temp = temp.replace(char, '') #REMOVES SPACES
temp = "".join(filter(lambda char: char in string.printable, temp)) #REMOVES NON ASCII CHARACTERS
name = ''.join(temp.split())
name = name[:random.randint(5,7)] #KEEPS 5 TO 7 LETTERS OF THE ORIGINAL STRING


randomNumber = random.randint(10000,99999)

dirname = os.path.dirname(__file__)
text_file_path = os.path.join(dirname, 'namesforreddit.txt')
text_file = open(text_file_path, "a")
text_file.write("USR: " + name + str(randomNumber) + " PWD: " + password) #OUTPUTS NAME AND NUMBER
text_file.write("\n")
text_file.close()

finalName = name+str(randomNumber)
time.sleep(1)
# NAME GENERATION FINISHED

# REDDIT ACCOUNT CREATION
driver.get(url)
driver.find_element(By.ID, 'regEmail').send_keys('mail@mail.mail')
time.sleep(1)
driver.find_element(By.XPATH, "//button[contains(text(),'Fortsetzen')]").click()
time.sleep(3)
driver.find_element(By.ID, 'regUsername').send_keys(finalName)
driver.find_element(By.ID, 'regPassword').send_keys(password)

#WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-checkmark")))
time.sleep(10)
sitekey = driver.find_element(By.XPATH,'/html/body/script[1]').get_attribute('outerHTML')
sitekey_clean= sitekey.split("""';

                window.___r""")[0].split("window.___grecaptchaSiteKey = '")[1]
print(sitekey)
print (sitekey_clean)
try:
    result = solver.recaptcha(
        sitekey=sitekey_clean,
        url=url)

except Exception as e:
    sys.exit(e)

else:
    print('result: ' + str(result))

    
    result1= result['code']
    print(result1)
    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

    driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", result1)
    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')

    driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div[3]/button').click()
    
    time.sleep(5)


# driver.close()
