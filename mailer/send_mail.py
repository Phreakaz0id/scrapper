import base64
import sendgrid
import os
import json

from logzero import logger, logfile
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(os.environ.get('FROM_EMAIL'))
to_emails = json.loads(os.environ.get("TO_EMAILS"))

subject = "Shops Scrapping"
content = Content("text/plain", "Perfumería y Limpieza")
mail = Mail(
    from_email=from_email,
    to_emails=to_emails,
    subject=subject,
    plain_text_content=content
)

files = os.listdir(os.path.dirname(__file__) + "/../output")

for _file in files:
    file_location = os.path.dirname(__file__) + f"/../output/{_file}"
    with open(file_location, 'rb') as f:
        data = f.read()
        f.close()

    encoded_data = base64.b64encode(data).decode()
    attachment = Attachment(
        FileContent(encoded_data),
        FileName(_file),
        FileType('application/csv'),
        Disposition('attachment')
    )
    mail.add_attachment(attachment)

if files == []:
    logger.error("No shops to scrap.")
else:
    logger.info(f"Sending email with files attached: {', '.join(files)}.")
    # exit()

    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)
