# force git
import imaplib
import email
import email.utils
import time
import uuid
import smtplib
import PyPDF2
from rtf_converter import rtf_to_txt

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import decode_header

import os
import json

import main

MODE = 'EMAIL'  # EMAIL or MICROPHONE or FORCE AUDIO or FORCE TEXT
FORCED_TEXT_FILENAME = "transcription.txt"
FORCED_AUDIO_FILENAME = "54 Clay Brook Rd 2.m4a"
WORK_TO_DO_DIR = "work-to-do"

email_pass = main.email_pass
email_user = main.email_user


def write_text_file(text, filepath):
    with open(filepath, "w") as f:
        f.write(text)
    return


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


def write_json_from_text_filepath(from_email, text_filepath):
    with open(text_filepath, "r") as f:
        text = f.read()

    json_dict = {
        "from": from_email,
        "text": text
    }

    guid_str = str(uuid.uuid4())
    guid_filename = f"file_{guid_str}.json"
    guid_filepath = WORK_TO_DO_DIR + "/" + guid_filename

    # Writing data to a JSON file using json.dump()
    with open(guid_filepath, "w") as json_file:
        json.dump(json_dict, json_file)

    return guid_filepath


def send_error_response_and_cleanup(filepath, work_filepath, from_email):
    send_email(from_email,
               "Invalid Request",
               "Request must have one and only one M4A, WAV, PDF, RTF or TXT attachment.",
               []
               )
    if os.path.exists(filepath):
        os.remove(filepath)

    if os.path.exists(work_filepath):
        os.remove(work_filepath)


def check_email_and_download():
    no_new_work_to_do = True
    while no_new_work_to_do:
        # Connect to Gmail's IMAP server
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        imap_server.login(email_user, email_pass)
        imap_server.select('inbox')

        # Search for all unread emails
        status, email_ids = imap_server.search(None, 'UNSEEN')

        if status == 'OK':
            email_id_list = email_ids[0].split()
            unread_count = len(email_id_list)

            if unread_count > 0:
                print(f"Number of unread emails: {unread_count}")
                attachment_dir = 'email_attachments'
                if not os.path.exists(attachment_dir):
                    os.mkdir(attachment_dir)

                # Fetch and download attachments from each unread email

                from_email = "lars@larsperkins.com"
                work_filepath = ""

                for email_id in email_id_list:
                    valid_attachments = 0
                    _, msg_data = imap_server.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    from_email = email.utils.parseaddr(msg.get("From"))[1]

                    # Decode the email subject
                    if isinstance(msg, dict) and len(decode_header(msg["Subject"])) > 0:
                        subject, encoding = decode_header(msg["Subject"])[0]
                    else:
                        subject = ""
                        encoding = None

                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    # Process attachments

                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        filename = part.get_filename().upper()
                        filepath = ""

                        if filename:
                            if filename.endswith((".M4A", ".WAV", ".TXT", ".PDF", ".RTF")):
                                valid_attachments += 1
                                if valid_attachments == 1:
                                    filepath = os.path.join(attachment_dir, filename)
                                    with open(filepath, 'wb') as f:
                                        f.write(part.get_payload(decode=True))
                                    print(f"Downloaded attachment: {filename}")

                                    root_filepath, _ = os.path.splitext(filepath)
                                    transcription_filename = root_filepath + ".TXT"

                                    if filename.endswith((".M4A", ".WAV")):
                                        main.transcribe_audio(filepath, transcription_filename)

                                    elif filename.endswith(".PDF"):
                                        text = convert_pdf_to_txt(filepath)
                                        write_text_file(text, transcription_filename)

                                    elif filename.endswith(".RTF"):
                                        text = convert_rtf_to_txt(filepath)
                                        write_text_file(text, transcription_filename)

                                    work_filepath = write_json_from_text_filepath(from_email, transcription_filename)
                                    if os.path.exists(filepath):
                                        os.remove(filepath)
                                    no_new_work_to_do = False
                                else:
                                    send_error_response_and_cleanup(filepath, work_filepath, from_email)
                        else:
                            send_error_response_and_cleanup(filepath, work_filepath, from_email)
        else:
            print("Failed to retrieve unread emails.")

        imap_server.logout()
        if no_new_work_to_do:
            time.sleep(30)

    return


def send_email(recipient_email, subject, body, attachments):
    # Set the sender and recipient email addresses
    sender_email = email_user
    receiver_email = recipient_email
    password = email_pass

    # Set the subject and body of the email
    # subject = "Evaluation of Investment Opportunity"
    # body = "See attachments."

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
