import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
from core.config import get_settings


def send_message(email, content):
    sg = sendgrid.SendGridAPIClient(
        # apikey=get_settings().sen
        api_key='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'
    )
    from_email = Email("practix@yandex.ru")
    to_email = Email(email)
    subject = "Письмо от PRACTIX"
    content = Content(
        "text/html", content
    )
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
