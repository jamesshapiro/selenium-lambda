import boto3
import os
import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json

website_url = os.environ['URL']
test_username = os.environ['TEST_USERNAME']
test_password = os.environ['TEST_PASSWORD']

def exit_gracefully():
    response_code = 200
    response = {
        'statusCode': response_code,
        'body': json.dumps({'shalom': 'haverim!'})
    }
    return response

class WebDriver(object):
    def __init__(self):
        self.options = Options()
        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--enable-javascript')
    def get(self):
        print("self.options")
        print(self.options.__dir__())
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver

def selenium(website_url):
    instance_ = WebDriver()
    driver = instance_.get()
    driver.get(f'https://{website_url}/login')
    
    inputs = driver.find_elements(By.CLASS_NAME, "amplify-input")
    username = inputs[0]
    password = inputs[1]
    username.send_keys(test_username)
    password.send_keys(test_password)
    WebDriverWait(driver=driver, timeout=5).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    #error_message = "Incorrect username or password."
    title = driver.title
    #print("[+] Login successful")
    driver.close()
    return {
        'statusCode': 200,
        'body': json.dumps(title)
    }

def lambda_handler(event, context):
    print('running')
    selenium(website_url)
    return exit_gracefully()