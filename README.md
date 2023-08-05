# WiFi Password Extractor

This script extracts saved WiFi passwords on a Windows machine and emails them to the user.

## Usage

1. Clone the repository
2. Create a `.env` file in the root of the cloned directory with your email credentials:

```
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password 
```

3. Run the script:

```
python wifi_password_extractor.py
```

The script will:

- Get a list of WiFi profile names using `netsh wlan`
- Extract the password for each profile using `netsh wlan show profile` 
- Email the list of SSIDs and passwords to the EMAIL_USER

The script uses Python 3 and the following libraries:

- subprocess
- re
- smtplib 
- email
- dotenv (install use ```pip install python-dotenv```)

## Notes

- The script only works on Windows due to using `netsh wlan`
- It extracts saved WiFi passwords, NOT passwords entered on connection
- On first run you may need to allow less secure apps in Gmail if using a Gmail account
- Be careful how you use and store the WiFi passwords extracted
- Do not commit the `.env` file to source control

Overall this provides a simple example of using Python to extract useful information from a system and send it to a user. While WiFi passwords, use responsibly!
