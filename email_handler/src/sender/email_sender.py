import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To
from core.config import get_settings


def send_message(email, content):
    sg = sendgrid.SendGridAPIClient(api_key='SENDGRID_API_KEY=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')
    from_email = Email("test@example.com")  # Change to your verified sender
    to_email = To("test@example.com")  # Change to your recipient
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)