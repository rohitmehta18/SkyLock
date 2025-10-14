Markdown

# Digital Security System with Remote Access

![Project Banner](https://placehold.co/1200x300/000000/FFFFFF?text=Digital%20Security%20System&font=montserrat)

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

A smart, real-time surveillance application that uses facial recognition to identify known and unknown individuals. The system automatically captures images of unknown persons, sends instant email alerts with photographic evidence, and allows for a remote PC lockdown via a secret email command.


## Core Features

-   **📸 Real-time Face Recognition**: Utilizes your webcam to identify people in real-time.
-   **🧠 Dynamic Learning**: Learns to recognize people from a folder of images (`known_faces`). Add new images to easily teach the system new faces.
-   **🤖 Intelligent Unknown Person Alerts**: Detects faces that are not in the known database and triggers an alert protocol. It's smart enough to only trigger the alert once per unique unknown person.
-   **🖼️ Automated Image Capture**: When an unknown person is detected, the system automatically captures a burst of 5 high-resolution photos and saves them to a local `alert_folder`.
-   **📧 Instant Email Notifications**: Immediately sends the captured images to a designated email address, providing real-time evidence.
-   **🔐 Remote PC Lock via Email Command**: A powerful security feature that allows you to lock your computer remotely. By replying to an alert email with a secret command phrase, the system will instantly lock the Windows session (`Win + L`).
-   **🔒 Secure Credential Management**: All sensitive information (email addresses, passwords) is stored securely in a `.env` file, which is ignored by Git to prevent accidental exposure.

---

## How It Works

The operational flow is designed for autonomous security and remote control.

1.  **Launch**: The system starts, loading the facial encodings from the `known_faces` directory.
2.  **Background Listener**: A separate thread starts, securely logging into your Gmail account to listen for the remote lock command.
3.  **Real-time Scan**: The main program accesses the webcam and continuously scans for faces.
4.  **Identification**:
    * **Known Person**: If a face is recognized, a green "match" box is drawn around them.
    * **Unknown Person**: If a face is not recognized, the alert protocol is initiated.
5.  **Alert Protocol**:
    * The system checks if this is a **new** unknown person it hasn't seen before in this session.
    * If new, it captures 5 photos and saves them to the `alert_folder`.
    * It then sends these 5 images as attachments in an email to your designated recipient address.
6.  **Remote Action**:
    * You receive the email on your phone or another device.
    * You reply with the secret command (e.g., `LOCKDOWN_NOW`).
    * The background listener on the host PC detects the command in your reply and immediately locks the computer.

---

## 📂 Project Structure

The project is organized into modular Python files for clarity and maintainability.

/digital_security_system/
|
|-- 📂 known_faces/
|   |-- person_one.jpg
|   |-- person_two.png
|
|-- 🐍 main.py             # Main application entry point
|-- 🐍 config.py           # All configurations and settings
|-- 🐍 face_utils.py       # Handles loading of known faces
|-- 🐍 alert_system.py     # Handles capturing alert images
|-- 🐍 email_alert.py      # Handles sending email notifications
|-- 🐍 email_checker.py    # Background service to check for remote commands
|-- 🐍 lock_pc.py          # Utility to lock the Windows PC
|
|-- 📜 .env                # Stores all secret credentials (you must create this)
|-- 📜 .gitignore          # Ensures .env is not tracked by Git
|-- 📜 requirements.txt     # Lists all necessary Python libraries
|-- 📜 README.md           # This file


---

## 🛠️ Setup and Installation Guide

Follow these steps carefully to get the project running.

### 1. Prerequisites

-   Python 3.9 or higher.
-   A Windows operating system (for the PC lock feature).
-   A webcam.

### 2. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/digital-security-system.git](https://github.com/YOUR_USERNAME/digital-security-system.git)
cd digital-security-system
3. Set Up a Virtual Environment (Recommended)
Bash

 Create a virtual environment
python -m venv .venv

Activate it
On Windows:
.venv\Scripts\activate
4. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
5. Configure Known Faces
Place image files (.jpg, .png) of people you want the system to recognize inside the known_faces folder.

Important: Rename each image file to the name of the person (e.g., john_doe.jpg, jane_doe.png).

6. Configure Gmail for Remote Access
You must configure your Gmail account to allow the application to send and receive emails.

a) Enable IMAP Access:

Go to your Gmail settings -> Forwarding and POP/IMAP.

Under IMAP access, select Enable IMAP.

Save changes.

b) Generate an App Password:

You cannot use your regular Gmail password. You must generate a special 16-digit App Password.

Go to your Google Account settings -> Security.

Ensure 2-Step Verification is turned ON.

Go to App Passwords.

For "Select app," choose Mail. For "Select device," choose Windows Computer.

Click Generate and copy the 16-digit password.

7. Create and Configure the .env File
In the main project directory, create a new file named .env.

Fill in your details, including the 16-digit App Password you just generated.

 --- Email Credentials ---
 Fill in your sender email and the recipient email.
IMPORTANT: Paste your 16-character Google App Password here.

EMAIL_SENDER="your__email@gmail.com"
EMAIL_PASSWORD="the_16__digit_app_password"
EMAIL_RECIPIENT="recipient__email@example.com"