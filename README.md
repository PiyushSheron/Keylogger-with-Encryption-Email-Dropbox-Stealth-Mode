# Keylogger with Encryption, Email, Dropbox & Stealth Mode

## 📌 Overview
This keylogger records keystrokes, encrypts the logs, and sends them securely via **email and Dropbox**. It runs **in stealth mode on Windows**, making it undetectable in normal processes. The script also has a **self-destruct feature** to erase traces upon termination.

## 🚀 Features
- **🔑 Keystroke Logging** – Captures all keystrokes in real time
- **🔒 Encrypted Logs** – Uses `cryptography` to encrypt keystrokes
- **📧 Email Delivery** – Sends logs to a specified email at intervals
- **☁ Dropbox Upload** – Uploads encrypted logs to Dropbox
- **🕵️ Stealth Mode** – Hides the script from process lists (Windows only)
- **💣 Self-Destruct** – Deletes all logs and itself upon manual termination

## 📦 Dependencies
Before running the script, install the required Python libraries:
```bash
pip install pynput cryptography dropbox
```

## ⚙️ Setup
1. **Configure Email Settings**:
   - Replace `EMAIL_ADDRESS`, `EMAIL_PASSWORD`, and `SEND_TO` with your email credentials.
   - If using Gmail, enable **App Passwords** or **Less Secure Apps**.

2. **Configure Dropbox Access**:
   - Generate a **Dropbox API access token** from [Dropbox Developer Console](https://www.dropbox.com/developers/apps).
   - Replace `DROPBOX_ACCESS_TOKEN` in the script.

## 🚀 Running the Keylogger
Run the script using:
```bash
python keylogger.py
```

On **Windows**, it will start in **stealth mode**. Logs will be encrypted and sent to the configured email and Dropbox.

## ⚠️ Disclaimer
This tool is for **educational and security awareness purposes only**. **Unauthorized use of keyloggers is illegal**. Ensure you have **explicit permission** before deploying it on any system.

🔒 **Stay ethical and secure!**

