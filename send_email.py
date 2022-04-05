from typing import List
import smtplib

gmail_user = 'coe817finalproject@gmail.com'
gmail_password = 'Test#2022'
to = ['coe817finalproject2@gmail.com']

def send_email(body: str):
    print(body)
    subject = 'Order'

    email_text = """\
    From: %s,
    To: %s,
    Subject: %s

    %s
    """ % (gmail_user, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)