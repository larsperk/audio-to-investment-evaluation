import imaplib
import email
from email.header import decode_header
import os
import json

import main

# Your Gmail credentials
email_pass = main.email_pass
email_user = main.email_user


def check_email_and_download():

    # Connect to Gmail's IMAP server
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(email_user, email_pass)
    imap_server.select('inbox')

    # Search for all unread emails
    status, email_ids = imap_server.search(None, 'UNSEEN')

    if status == 'OK':
        email_id_list = email_ids[0].split()
        print(f"Number of unread emails: {len(email_id_list)}")

        # Create a directory to store attachments
        attachment_dir = 'email_attachments'
        if not os.path.exists(attachment_dir):
            os.mkdir(attachment_dir)

        # Fetch and download attachments from each unread email
        for email_id in email_id_list:
            _, msg_data = imap_server.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            # Process attachments
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename:
                    filepath = os.path.join(attachment_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded attachment: {filename}")

            imap_server.store(email_id, '+FLAGS', '(\Seen)')

    else:
        print("Failed to retrieve unread emails.")

# Logout and close the connection
imap_server.logout()

data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Specify the file path where you want to write the JSON data
file_path = "data.json"

# Writing data to a JSON file using json.dump()
with open(file_path, "w") as json_file:
    json.dump(data, json_file)

print("Data has been written to", file_path)