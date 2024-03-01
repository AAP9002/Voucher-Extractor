import time
import requests
import urllib.parse
import random
import string
import hashlib
import re
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from PIL import Image
from dotenv import load_dotenv, dotenv_values
from tqdm import tqdm

load_dotenv()
config = dotenv_values(".env")

DOMAIN = config["DOMAIN"]
APIKEY = config["RAPIDKEY"]
APILIMIT = config["APILIMIT"]
EXPRECTEDSUBJECT = config["EXPRECTEDSUBJECT"]

def extract_id(text):
    # Regular expression to match URLs
    url_pattern = r'https?://\S+'

    # Find URLs in the text
    urls = re.findall(url_pattern, text)

    # Extract and print the ID from each URL
    for url in urls:
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        id = query_parameters.get('id', [None])[0]
        print("URL:", url)
        print("ID:", id)
        if id is not None:
            return id
    return None

def call_api(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    driver.quit()

def sleep():
    duration = random.randint(5, 10)
    time.sleep(duration)

class emailService:
    def __init__(self):
        self.callCount = 0

    def create_email(self):
        url = "https://temp-mail44.p.rapidapi.com/api/v3/email/new"
        payload = {
            "key1": "value",
            "key2": "value"
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": APIKEY,
            "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        self.callCount += 1

        print("Email Created: ")
        print(response.json())
        self.email_address = response.json()['email']

    def get_email(self):
        return self.email_address

    def get_call_count(self):
        return self.callCount

    def get_email_list(self, manual_email = None):
        if manual_email is not None:
            self.email_address = manual_email
        
        url = "https://temp-mail44.p.rapidapi.com/api/v3/email/"+self.email_address+"/messages"

        headers = {
            "X-RapidAPI-Key": APIKEY,
            "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            self.callCount += 1
            # print(response.json())

            subject = response.json()[-1]['subject']
            if subject == EXPRECTEDSUBJECT:
                body = response.json()[-1]['body_text']
                print("Email Found")
                # print("Email Subject: " + subject)
                # print("Email Body: " + body)
                return extract_id(body)
            return None
        except Exception as e:
            print("error:", e)
            return None

class FfHandler:
    def sign_up_account(self, email):
        signUpAPI = DOMAIN + '/includes/mailing_list/join-club.php?email_address=' + email
        call_api(signUpAPI)
        print("Account Created")

    def confirm_account(self, email, tempId):
        confirmEmail = DOMAIN + '/confirm-mailing-list?action=confirm&id='+tempId+'&email_address='+email
        call_api(confirmEmail)
        print("Account Confirmed")

    def unsubscribe_account(self, email, tempId):
        unsubscribe = DOMAIN + '/confirm-mailing-list?action=unsubscribe_confirm&id='+tempId+'&email_address='+email
        call_api(unsubscribe)
        print("Account Unsubscribed")

    def take_screenshot(self, email, tempId, output_file):
        url = DOMAIN + '/Vouchers?id='+tempId+'&email_address='+email
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options)
        driver.set_window_size(1920, 1080)
        driver.get(url)
        driver.save_screenshot(output_file)
        driver.quit()
        print("Screenshot Taken")

    def getVouchers(self, imageFile, output_file):
        im = Image.open(imageFile)
        im = im.crop((330, 420, 1250, 725))
        im.save(output_file)
        print("Vouchers Extracted")

target_count = int(input("Enter the number of accounts to create (MAX 80 A DAY): "))
call_count_hard_limit = int(input("Enter the hard limit of API calls (-1 for default of "+APILIMIT+"): "))

if call_count_hard_limit != -1:
    APILIMIT = call_count_hard_limit

progress_bar = tqdm(total=target_count, desc="Progress", position=0, leave=True, dynamic_ncols=True)

eS = emailService()
ff = FfHandler()
eS.create_email()

count = 0

while (count<target_count) and (eS.get_call_count() < APILIMIT):
    ff.sign_up_account(eS.get_email())
    sleep()
    id = eS.get_email_list()
    if id is not None:
        ff.confirm_account(eS.get_email(), id)
        sleep()
        ff.take_screenshot(eS.get_email(), id, 'bin/ss.png')
        ff.getVouchers('bin/ss.png', 'bin/image_temp/'+str(count)+'.png')
        count += 1
        progress_bar.update(1)
        sleep()
        ff.unsubscribe_account(eS.get_email(), id)
        sleep()
    else:
        print("No email found")
        sleep()
        continue

progress_bar.close()
print("All Completed")
