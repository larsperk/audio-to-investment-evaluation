import imaplib
import email
import os
import time
import email.utils
import smtplib
import PyPDF2

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from rtf_converter import rtf_to_txt
from email.header import decode_header

import main

email_pass = main.email_pass
email_user = main.email_user

def check_email_and_download():

    # Connect to the server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to the account
    mail.login(email_user, email_pass)

    # Select the mailbox
    mail.select("inbox")

    # Get uids
    result, data = mail.uid("search", None, "ALL")
    if result == "OK":
        uids = data[0].split()
        last_email_uid = uids[-1]

    def download_attachment(msg):
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if bool(filename):
                filepath = os.path.join(os.getcwd(), filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                return filepath
        return None

    def convert_pdf_to_txt(pdf_path):
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Initialize text variable to store all content
            plain_text = ""

            # Loop through all pages and extract text
            for i in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[i]
                plain_text += page.extract_text()

        return plain_text

    def convert_rtf_to_txt(rtf_path):
        with open(rtf_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()

        # Convert RTF content to plain text
        plain_text = rtf_to_txt(rtf_content)
        return plain_text

    while True:
        # Reconnect and select the inbox
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")

        # Search for new emails
        result, data = mail.uid("search", None, "ALL")
        if result == "OK":
            uids = data[0].split()
            new_email_uid = uids[-1]

            if last_email_uid != new_email_uid:
                # Fetch the new email
                result, data = mail.uid("fetch", new_email_uid, "(RFC822)")
                if result == "OK":
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    from_email = email.utils.parseaddr(msg.get("From"))[1]
                    subject, encoding = decode_header(msg["subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    # Download attachment
                    filepath = download_attachment(msg)

                    if filepath.lower().endswith((".wav", ".m4a", ".txt")):
                        return from_email, filepath
                    elif filepath.lower().endswith(".rtf"):
                        base, extension = os.path.splitext(filepath)
                        output_file = main.TRANSCRIPTION_FILENAME
                        text = convert_rtf_to_txt(filepath)
                        with open(output_file, 'w') as file:
                            file.write(text)
                        return from_email, base + ".txt"
                    elif filepath.lower().endswith(".pdf"):
                        base, extension = os.path.splitext(filepath)
                        output_file = main.TRANSCRIPTION_FILENAME
                        text = convert_pdf_to_txt(filepath)
                        with open(output_file, 'w') as file:
                            file.write(text)
                        return from_email, base + ".txt"

                last_email_uid = new_email_uid

        # Sleep for a while and then check again
        time.sleep(10)


def send_email(recipient_email, attachments):
    # Set the sender and recipient email addresses
    sender_email = email_user
    receiver_email = recipient_email
    password = email_pass

    # Set the subject and body of the email
    subject = "Evaluation of Investment Opportunity"
    body = "See attachments."

    # Create a multipart email
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = subject
    email.attach(MIMEText(body, "plain"))

    for attachment_file in attachments:
        # Open the file in binary mode and create a MIME object
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode the payload and add the necessary headers
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_file}",
        )

        # Attach the MIME object to the email
        email.attach(part)

    # Set up the server and port
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Log into the server
    server.starttls()  # Start the TLS (Transport Layer Security) mode to encrypt the session
    server.login(sender_email, password)

    # Send the email
    text = email.as_string()  # Convert the MIMEMultipart object to a string
    server.sendmail(sender_email, receiver_email, text)

    # Quit the server
    server.quit()
