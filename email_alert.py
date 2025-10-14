import os
import smtplib
import ssl
import threading  # --- NEW: Import the threading library ---
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import config

def send_email_with_alert(image_filenames):
    """Sends the initial 5 face pictures in a background thread."""
    sender = config.EMAIL_SENDER
    password = config.EMAIL_PASSWORD
    recipient = config.EMAIL_RECIPIENT

    if not all([sender, password, recipient]):
        print("❌ Error: Email credentials not found.")
        return

    print("   -> Preparing to send photo alert...")
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"🚨 Security Alert: Unknown Person Detected"
    timestamp = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')
    body = f"An unknown person was detected on {timestamp}.\n\nPlease review the attached images."
    msg.attach(MIMEText(body, 'plain'))

    for filename in image_filenames:
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
            msg.attach(part)
        except FileNotFoundError:
            print(f"      Error attaching file: {filename} not found.")
            continue
            
    # --- UPDATED: Also send this email in a background thread for responsiveness ---
    email_thread = threading.Thread(target=_send_email_in_background, args=(sender, recipient, msg, "Photo alert"))
    email_thread.start()


def send_screenshot_report(screenshot_filenames):
    """Sends all collected screenshots in a background thread."""
    if not screenshot_filenames:
        print("[Email] No screenshots to send. Skipping report.")
        return

    sender = config.EMAIL_SENDER
    password = config.EMAIL_PASSWORD
    recipient = config.EMAIL_RECIPIENT

    if not all([sender, password, recipient]):
        print("❌ Error: Email credentials not found.")
        return

    print(f"   -> Preparing to send screenshot report with {len(screenshot_filenames)} images...")
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"📊 Security Report: {len(screenshot_filenames)} Screenshots Attached"
    timestamp = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')
    body = f"Following an unknown face alert, the system captured the attached screenshots.\n\nMonitoring stopped at {timestamp}."
    msg.attach(MIMEText(body, 'plain'))

    for filename in screenshot_filenames:
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
            msg.attach(part)
        except FileNotFoundError:
            print(f"      Error attaching screenshot: {filename} not found.")
            continue
    
    email_thread = threading.Thread(target=_send_email_in_background, args=(sender, recipient, msg, "Screenshot report"))
    email_thread.start()


def _send_email_in_background(sender, recipient, msg, alert_type):
    """Helper function to send email in a non-blocking thread."""
    smtp_server = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, config.EMAIL_PASSWORD)
            server.sendmail(sender, recipient, msg.as_string())
            print(f"✅ {alert_type} email sent successfully!")
    except Exception as e:
        print(f"      ❌ An error occurred while sending the {alert_type} email: {e}")