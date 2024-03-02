import time
import random
import re
import requests
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from PIL import Image
from dotenv import load_dotenv, dotenv_values
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
import sys


load_dotenv()
config = dotenv_values(".env")

DOMAIN = config["DOMAIN"]
APIKEY = config["RAPIDKEY"]
EXPRECTEDSUBJECT = config["EXPRECTEDSUBJECT"]

MIN_DELAY = 5
MAX_DELAY = 10

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
        # print("URL:", url)
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
    duration = random.randint(MIN_DELAY, MAX_DELAY)
    time.sleep(duration)


class emailService:
    def __init__(self):
        self.email_address = ""

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
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 429:
                print("########## API Limit Reached ##########")
                exit()
            self.email_address = response.json()['email']
            print("Email Created: "+self.email_address)
        except Exception as e:
            print("error:", e)
            exit(1)

    def get_email(self):
        return self.email_address

    def get_email_list(self, manual_email = None):
        if manual_email is not None:
            self.email_address = manual_email

        url = "https://temp-mail44.p.rapidapi.com/api/v3/email/"+self.email_address+"/messages"

        headers = {
            "X-RapidAPI-Key": APIKEY,
            "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com"
        }

        for i in range(3): # Retry 3 times
            try:
                response = requests.get(url, headers=headers)

                if response.status_code == 429:
                    print("########## API Limit Reached ##########")
                    exit(1)

                subject = response.json()[-1]['subject']
                if subject == EXPRECTEDSUBJECT:
                    body = response.json()[-1]['body_text']
                    print("Email Found")
                    # print("Email Subject: " + subject)
                    # print("Email Body: " + body)
                    return extract_id(body)
            except Exception as e:
                print("error:", e)
            print("Retrying in 10 seconds...")
            time.sleep(10)
        return None

class FfHandler:
    def sign_up_account(self, email):
        sign_up_api = DOMAIN + '/includes/mailing_list/join-club.php?email_address=' + email
        call_api(sign_up_api)
        print("Account Created")

    def confirm_account(self, email, temp_id):
        confirm_email = DOMAIN + '/confirm-mailing-list?action=confirm&id='+temp_id+'&email_address='+email
        call_api(confirm_email)
        print("Account Confirmed")

    def unsubscribe_account(self, email, temp_id):
        unsubscribe = DOMAIN + '/confirm-mailing-list?action=unsubscribe_confirm&id='+temp_id+'&email_address='+email
        call_api(unsubscribe)
        print("Account Unsubscribed")

    def take_screenshot(self, email, temp_id, output_file):
        url = DOMAIN + '/Vouchers?id='+temp_id+'&email_address='+email
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options)
        driver.set_window_size(1920, 1080)
        driver.get(url)
        driver.save_screenshot(output_file)
        driver.quit()
        print("Screenshot Taken")

    def get_vouchers(self, image_file, output_file):
        im = Image.open(image_file)
        im = im.crop((330, 420, 1250, 725))
        im.save(output_file)
        print("Vouchers Extracted")

target_count = int(input("Enter the number of accounts to create (MAX 99 A DAY): "))

print("Starting...")

eS = emailService()
ff = FfHandler()
eS.create_email()

with Progress(
    SpinnerColumn(),
    *Progress.get_default_columns(),
    TimeElapsedColumn(),
    ) as progress:
    wholeProgress = progress.add_task("[green]Jobs...", total=target_count)

    for i in range(target_count):
        taskProgress = progress.add_task("[cyan1]Voucher "+str(i+1)+"/"+str(target_count)+"...", total=5)
        ff.sign_up_account(eS.get_email())
        progress.update(taskProgress, advance=1)
        sleep()

        user_id = eS.get_email_list()
        if user_id is not None:
            ff.confirm_account(eS.get_email(), user_id)
            progress.update(taskProgress, advance=1)
            sleep()

            ff.take_screenshot(eS.get_email(), user_id, 'bin/ss.png')
            progress.update(taskProgress, advance=1)

            ff.get_vouchers('bin/ss.png', 'bin/image_temp/'+str(i)+'.png')
            progress.update(taskProgress, advance=1)
            sleep()

            ff.unsubscribe_account(eS.get_email(), user_id)
            progress.update(taskProgress, advance=1)
            if i != target_count-1:
                sleep()
        else:
            print("No email found")
            exit()

        progress.remove_task(taskProgress)
        progress.update(wholeProgress, advance=1)

print("All Completed")
print("\a")
time.sleep(0.5)
print("\a")
time.sleep(0.5)
print("\a")