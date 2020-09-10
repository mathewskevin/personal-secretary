import os

# generate today's schedule
import schedule

# generate summary email body
schedule.html_message()

# get email body text, data, etc.
import schedule_email_data

# SELECT MODE
message_dict = schedule_email_data.email_test # TEST MODE
#message_dict = schedule_email_data.email_dict # PRODUCTION MODE

# Using SendGrid's Python Library
# https://www.twilio.com/blog/sending-email-attachments-with-twilio-sendgrid-python
from dotenv import load_dotenv
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

project_folder = '/'.join(os.path.abspath(__file__).split('/')[:~0])
load_dotenv(os.path.join(project_folder, 'sendgrid.env'))

# load email list
email_list = message_dict.keys()

# send emails
for email in email_list:
    mid_dict = message_dict.get(email)

    message = Mail(
    from_email=mid_dict.get('email'),
    to_emails=email,
    subject=mid_dict.get('subject'),
    html_content=mid_dict.get('email_text'))

    with open(r'summary.txt', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('summary.txt'),
        FileType('application/txt'),
        Disposition('attachment')
        )
    message.attachment = attachedFile

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    #sg = SendGridAPIClient(schedule_email_data.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
    print(email)
