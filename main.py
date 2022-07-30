import time
import hashlib
import ssl
import smtplib
from email.message import EmailMessage
from getpass import getpass
from urllib.request import urlopen, Request
from datetime import datetime

# This project was inspired by this tutorial:
# https://www.geeksforgeeks.org/python-script-to-monitor-website-changes/

# Specify the email address for your sending email account (Check Readme for prerequisites)
sender = "yourname@gmail.com"
# Specify the receiver email address (No prerequisites)
receiver = "receiver@mail.com"
# Specify the Website url you want to check for changes
url = "https://your-website.xyz/"
# Specify the time between website-checks (in Seconds)
wait_time = 3600


def send_mail(password):
    """
    Sends an email from the sender email account to the receiver with the specified "subject" and "body"

    Parameter(s):
        password (String): The password / token for your sender email account
    """
    # Change the subject of the mail
    subject = "An update on the website you are monitoring was detected!"
    # Change the body of the mail
    body = "Update on the website with the url: " + url + " was detected!"

    e = EmailMessage()
    e["From"] = sender
    e["To"] = receiver
    e["Subject"] = subject
    e.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, e.as_string())
        print("Email sent!")


def main():
    # Prints the current settings
    print("----------")
    print("Website Checker running with: ")
    print("Current Website URL: ", url)
    print("Current time between Website checks: ", wait_time)
    password = getpass("Please enter the password / token for the sender Email Account: ")
    print("----------")

    # Get the Website data
    r = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(r).read()

    # Create initial Hash
    current_hash = hashlib.sha224(response).hexdigest()

    time.sleep(10)

    # Check for website Updates until the script is interrupted by the user
    while 1:
        try:
            # Create Hash 1
            response = urlopen(r).read()
            current_hash = hashlib.sha224(response).hexdigest()

            # The time that has to pass before a new Hash is created
            time.sleep(wait_time)

            # Create Hash 2
            response = urlopen(r).read()
            new_hash = hashlib.sha224(response).hexdigest()

            # Check if Hash 1 == Hash 2 <=> If the Website has changed
            if current_hash == new_hash:
                print("No update detected")
                continue
            else:
                # Get the time & date information
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                current_date = now.date()

                print("Website update detected at: [" + str(current_date) + "] " + current_time + "!")
                # Sends an Email when there is *ANY* change to the website
                send_mail(password)

                response = urlopen(r).read()
                current_hash = hashlib.sha224(response).hexdigest()
                time.sleep(wait_time)
                continue

        except Exception:
            print("[Debug] Error!")


if __name__ == '__main__':
    main()
