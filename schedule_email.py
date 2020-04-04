import os
from dotenv import load_dotenv
#project_folder = os.path.expanduser(os.getcwd())  # adjust as appropriate
project_folder = '/'.join(os.path.abspath(__file__).split('/')[:~0])
load_dotenv(os.path.join(project_folder, 'sendgrid.env'))

# generate summary file
import schedule
schedule.html_message()

# using SendGrid's Python Library
# https://www.twilio.com/blog/sending-email-attachments-with-twilio-sendgrid-python
import os
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

message = Mail(
    from_email='from_email@example.com', # from_email@example.com
    to_emails=os.environ.get('EMAIL_VAL'),
    subject='Secretary',
    html_content='<p>See todays schedule update.</p>')

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
response = sg.send(message)
print(response.status_code, response.body, response.headers)
