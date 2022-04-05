# -*- coding: utf-8 -*-
import imaplib
import email
from email.header import decode_header


# account credentials
username = "coe817finalproject2@gmail.com"
password = "Test#2022"

def accessEmail():

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    result, data = imap.search(None, 'SUBJECT', '"Order"')

    id_list = data[0].split()
    latest_email_id = id_list[-1]

    result_from_fetch, data_from_fetch = imap.fetch(latest_email_id, "(RFC822)")
    raw_email = data_from_fetch[0][1]
    raw_email_string = raw_email.decode("utf-8")

    email_message = email.message_from_string(raw_email_string)

    body = ""

    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=False)
        else:
            continue

    # close the connection and logout
    imap.close()
    imap.logout()

    return body