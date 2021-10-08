import os

from logzero import logger, logfile
from sendgrid.helpers.mail import *
from mailer.sendgrid_client import (
    build_attachment,
    build_content,
    prepare_email,
    send_email
)
from settings import (
    ADMIN_EMAILS,
    ATTACHMENTS_DIR,
    CLIENT_EMAILS,
    EXECUTION_TIMESTAMP,
    FAILURE_BODY,
    FAILURE_SUBJECT,
    MAIN_LOG_FILE,
    FROM_EMAIL,
    SUCCESS_BODY,
    SUCCESS_SUBJECT
)

MODULE = __name__


def prepare_and_send_email(to_emails, subject, body):
    logfile(MAIN_LOG_FILE)
    content = build_content("text/plain", body)
    mail = prepare_email(FROM_EMAIL, to_emails, subject, content)
    attach_files(mail)
    logger.info(f"""[{MODULE}] 📨 Sending email:
        from sender: {FROM_EMAIL}
        to recipients: {', '.join(to_emails)}
        subject: {subject}
        body: {body}
    """)
    response = send_email(mail)
    check_email_response(response)


def check_email_response(response):
    if (response.status_code == 202):
        logger.info(f"[{MODULE}] ✅ Succesfully sent email. Response: {response.__dict__}")
    else:
        logger.error(f"[{MODULE}] Unexpected error while sending email. Response: \n\n{response.__dict__}")


def attach_files(mail):
    try:
        files = list(
            filter(
                lambda f: EXECUTION_TIMESTAMP in f,
                os.listdir(os.path.dirname(__file__) + f"/../{ATTACHMENTS_DIR}")))

        if files == []:
            raise Exception("❌ The script has been scheduled but no attachments were found.")

        logger.info(f"[{MODULE}] Preparing the following attachments: {', '.join(files)}.")

        for file_name in files:
            file_location = os.path.dirname(__file__) + f"/../{ATTACHMENTS_DIR}/{file_name}"
            with open(file_location, 'rb') as f:
                data = f.read()
                f.close()

            logger.info(f"[{MODULE}] 📨 Preparing attachment for '{file_name}'.")
            attachment = build_attachment(file_name, data, "application/csv")
            mail.add_attachment(attachment)
            logger.info(f"[{MODULE}] 📨 {file_name} succesfully encoded to attachment.")

    except Exception as e:
        logfile(MAIN_LOG_FILE)
        logger.error(f"[{MODULE}] ❌ An unexpected error occured while reading attachments: \n\n{e}", exc_info=True)


def notify_clients():
    prepare_and_send_email(CLIENT_EMAILS, SUCCESS_SUBJECT, SUCCESS_BODY)


def notify_errors():
    prepare_and_send_email(ADMIN_EMAILS, FAILURE_SUBJECT, FAILURE_BODY)


if __name__ == "__main__":
    notify_clients()
