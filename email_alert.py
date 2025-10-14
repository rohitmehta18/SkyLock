import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Import our configuration
import config

# --- This is the function that main.py is looking for ---
def send_email_with_alert(image_filenames):
    """
    Sends an email with the captured alert images as attachments.
    """
    sender = config.EMAIL_SENDER
    password = config.EMAIL_PASSWORD
    recipient = config.EMAIL_RECIPIENT

    if not all([sender, password, recipient]):
        print("❌ Error: Email credentials not found in your .env file.")
        print("   -> Please ensure your .env file exists and contains EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECIPIENT.")
        return

    print("   -> Preparing to send email alert...")

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"🚨 Security Alert: Unknown Person Detected"

    # Add the email body
    timestamp = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')
    body = f"An unknown person was detected by the security system on {timestamp}.\n\nPlease review the attached images."
    msg.attach(MIMEText(body, 'plain'))

    # Attach each image
    for filename in image_filenames:
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f"attachment; filename= {os.path.basename(filename)}",
            )
            msg.attach(part)
        except FileNotFoundError:
            print(f"      Error attaching file: {filename} not found.")
            continue

    # Send the email using Gmail's SMTP server
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            print("✅ Email alert sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("      ❌ Error: SMTP Authentication Failed. Check your EMAIL_SENDER and EMAIL_PASSWORD.")
        print("      Remember to use a Google App Password, not your regular password.")
    except Exception as e:
        print(f"      ❌ An error occurred while sending the email: {e}")

