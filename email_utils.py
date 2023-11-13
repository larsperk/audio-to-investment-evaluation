import imaplib
import email
import email.utils
import time
import uuid
import smtplib
import PyPDF2
import docx2txt
from rtf_converter import rtf_to_txt
from pptx import Presentation
import docx
from docx.shared import RGBColor
from datetime import datetime

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


def convert_pptx_to_text(pptx_path):
    prs = Presentation(pptx_path)
    plain_text = ""

    # Iterate through each slide and its shapes to extract text
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                plain_text += shape.text + "\n"

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
               "Request must have one and only one M4A, WAV, PDF, RTF, PPTX, DOC or TXT attachment.",
               []
               )
    if os.path.exists(filepath):
        os.remove(filepath)

    if os.path.exists(work_filepath):
        os.remove(work_filepath)


def convert_txt_to_docx(summary_txt_file, evaluation_txt_file):
    filename_list = []
    with open(summary_txt_file, "r") as f:
        summary_txt_file_contents = [line.strip() for line in f]

    temp = []
    for line in summary_txt_file_contents:
        first_space = line.find(" ")
        if first_space > 1:
            left_of_space = line[:first_space]
            if left_of_space == left_of_space.upper() and left_of_space.endswith(":"):
                temp.append(left_of_space)
                temp.append(line[first_space+1:])
            else:
                temp.append(line)
        else:
            temp.append(line)

    summary_txt_file_contents = temp

    with open(evaluation_txt_file, "r") as f:
        evaluation_txt_file_contents = [line.strip() for line in f]

    company_name = main.get_name_of_company(summary_txt_file_contents[1])
    if company_name[:26].upper() == 'THE NAME OF THE COMPANY IS':
        company_name = company_name[27:]
    if company_name[:33].upper() == "THE INFORMATION PROVIDED DOES NOT":
        company_name = "Unknown"

    company_name = company_name or "UNKNOWN"

    docx_filename = write_docx_file("Summary", company_name, summary_txt_file_contents)
    filename_list.append(docx_filename)
    docx_filename = write_docx_file("Evaluation", company_name, evaluation_txt_file_contents)
    filename_list.append(docx_filename)

    return filename_list[0], filename_list[1]


def write_docx_file(output_file_prefix, company_name, text_file_contents):
    todays_datetime = datetime.now().strftime("%Y-%m-%d %H%M")
    doc = docx.Document()

    title = doc.add_paragraph(f"{output_file_prefix} of {company_name}\n{todays_datetime}")

    run = title.runs[0]
    run.font.size = docx.shared.Pt(14)
    run.font.bold = True

    line_numbering_is_on = False
    bulleting_is_on = False
    for line in text_file_contents:
        if line != "":
            if line.endswith(":") or (line == line.upper()):
                heading = doc.add_heading(line)
                run = heading.runs[0]
                run.font.size = docx.shared.Pt(14)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)
                line_numbering_is_on = not line_numbering_is_on and not bulleting_is_on

            elif output_file_prefix == "Evaluation":
                while line[:1] in "01234567890. ":
                    line = line[1:]
                if line_numbering_is_on:
                    doc.add_paragraph(line, style="List Number")
                else:
                    doc.add_paragraph(line, style="List Bullet")
                    bulleting_is_on = True

            else:
                graph = doc.add_paragraph(line)
                graph.paragraph_format.line_spacing = 1
                graph.paragraph_format.space_after = 0

    todays_datetime = datetime.now().strftime("%Y-%m-%d %H%M")
    docx_filename = f"{output_file_prefix}-{company_name}-{todays_datetime}.docx"
    doc.save(docx_filename)

    return docx_filename


def get_emails_and_create_work_files():
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
                main.log_message(f"Number of unread emails: {unread_count}")
                attachment_dir = 'email_attachments'
                if not os.path.exists(attachment_dir):
                    os.mkdir(attachment_dir)

                # Fetch and download attachments from each unread email
                work_filepath = ""

                for email_id in email_id_list:
                    valid_attachments = 0
                    _, msg_data = imap_server.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    from_email = email.utils.parseaddr(msg.get("From"))[1]

                    # Decode the email subject THIS WILL ALWAYS SHORT CIRCUIT - MSG IS NOT A DICT
                    try:
                        subject, encoding = decode_header(msg["Subject"])[0]

                    except:
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
                            if filename.endswith((".M4A", ".WAV", ".TXT", ".PDF", ".RTF", ".PPTX", ".DOCX")):
                                valid_attachments += 1
                                if valid_attachments == 1:
                                    filepath = os.path.join(attachment_dir, filename)
                                    with open(filepath, 'wb') as f:
                                        f.write(part.get_payload(decode=True))
                                    main.log_message(f"Downloaded attachment: {filename}")

                                    root_filepath, _ = os.path.splitext(filepath)
                                    transcription_filename = root_filepath + ".TXT"

                                    if filename.endswith((".M4A", ".WAV")):
                                        main.log_message("transcribe start")
                                        main.transcribe_audio_using_aai(filepath, transcription_filename)
                                        main.log_message("transcribe end")

                                    elif filename.endswith(".PDF"):
                                        text = convert_pdf_to_txt(filepath)
                                        write_text_file(text, transcription_filename)

                                    elif filename.endswith(".RTF"):
                                        text = convert_rtf_to_txt(filepath)
                                        write_text_file(text, transcription_filename)

                                    elif filename.endswith(".PPTX"):
                                        text = convert_pptx_to_text(filepath)
                                        write_text_file(text, transcription_filename)

                                    elif filename.endswith(".DOCX"):
                                        text = docx2txt.process(filepath)
                                        write_text_file(text, transcription_filename)

                                    work_filepath = write_json_from_text_filepath(from_email, transcription_filename)
                                    if os.path.exists(filepath):
                                        os.remove(filepath)
                                    no_new_work_to_do = False

                                    main.log_message("we got some work to do ...")

                                else:
                                    send_error_response_and_cleanup(filepath, work_filepath, from_email)
                        else:
                            send_error_response_and_cleanup(filepath, work_filepath, from_email)
        else:
            main.log_message("Failed to retrieve unread emails.")

        try:
            imap_server.logout()
        except:
            pass

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
    outbound_email = MIMEMultipart()
    outbound_email["From"] = sender_email
    outbound_email["To"] = receiver_email
    outbound_email["Subject"] = subject
    outbound_email.attach(MIMEText(body, "plain"))

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
        outbound_email.attach(part)

    # Set up the server and port
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Log into the server
    server.starttls()  # Start the TLS (Transport Layer Security) mode to encrypt the session
    server.login(sender_email, password)

    # Send the email
    text = outbound_email.as_string()  # Convert the MIMEMultipart object to a string
    server.sendmail(sender_email, receiver_email, text)

    # Quit the server
    server.quit()
