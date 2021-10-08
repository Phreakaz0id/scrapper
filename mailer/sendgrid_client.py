import base64
import os
import sendgrid

from sendgrid.helpers.mail import *

MODULE = __name__


def get_client():
    return sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))


def get_post_client():
    sg = get_client()
    return sg.client.mail.send.post


def prepare_email(from_email, to_emails, subject, content):
    return Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        plain_text_content=content
    )


def build_attachment(file_name, file_data, file_type):
    encoded_data = base64.b64encode(file_data).decode()
    return Attachment(
        FileContent(encoded_data),
        FileName(file_name),
        FileType(file_type),
        Disposition('attachment')
    )


def build_content(body, content_type):
    return Content(content_type, body)


def send_email(mail):
    post_client = get_post_client()
    return post_client(request_body=mail.get())
