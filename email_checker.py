import imaplib
import email
import time
from email.header import decode_header
import config
from lock_pc import lock_windows_pc

def check_email_for_lock_command(stop_event):
    """
    Periodically checks the email inbox for unread messages containing the lock command.
    This is a diagnostic version with detailed print statements.
    """
    print("[Email Checker] Thread started. Will check for commands every {} seconds.".format(config.EMAIL_CHECK_INTERVAL_SECONDS))
    
    while not stop_event.is_set():
        try:
            # --- DIAGNOSTIC PRINT ---
            print("\n[Email Checker] Attempting to connect to Gmail...")
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            
            # --- DIAGNOSTIC PRINT ---
            print(f"[Email Checker] Logging in as {config.EMAIL_SENDER}...")
            mail.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            mail.select("inbox")
            
            # --- DIAGNOSTIC PRINT ---
            search_query = f'(UNSEEN FROM "{config.EMAIL_RECIPIENT}")'
            print(f"[Email Checker] Searching inbox with query: {search_query}")
            status, messages = mail.search(None, search_query)

            if status == "OK":
                message_ids = messages[0].split()
                if not message_ids:
                    # --- DIAGNOSTIC PRINT ---
                    print("[Email Checker] No new unread messages found from the recipient.")
                else:
                    print(f"[Email Checker] ✅ Found {len(message_ids)} unread message(s) from recipient.")

                for msg_id in message_ids:
                    status, msg_data = mail.fetch(msg_id, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        break
                            else:
                                body = msg.get_payload(decode=True).decode()
                            
                            # --- DIAGNOSTIC PRINT ---
                            print("\n--- Start of Retrieved Email Body ---")
                            print(body)
                            print("--- End of Retrieved Email Body ---\n")
                            
                            # --- DIAGNOSTIC PRINT ---
                            print(f"[Email Checker] Checking for '{config.LOCK_COMMAND_WORD}' in the body...")
                            if config.LOCK_COMMAND_WORD in body:
                                print("[Email Checker] ✅ COMMAND FOUND! Initiating lock.")
                                lock_windows_pc()
                                mail.store(msg_id, '+FLAGS', '\\Seen') # Mark as read
                                break
                            else:
                                print("[Email Checker] ❌ Command NOT found in this email.")
                    else: continue
                    break
            else:
                print(f"[Email Checker] ❌ Failed to search inbox. Status: {status}")

            mail.logout()
            print("[Email Checker] Logged out successfully.")

        except imaplib.IMAP4.error as e:
            print(f"[Email Checker] ❌ CRITICAL IMAP Error: {e}")
            print("   -> This could be a wrong password, or IMAP is not enabled in Gmail settings.")
        except Exception as e:
            print(f"[Email Checker] ❌ An unexpected error occurred: {e}")

        # Wait for the specified interval before checking again
        print(f"[Email Checker] Waiting for {config.EMAIL_CHECK_INTERVAL_SECONDS} seconds...")
        time.sleep(config.EMAIL_CHECK_INTERVAL_SECONDS)
        
    print("[Email Checker] Thread stopped.")

