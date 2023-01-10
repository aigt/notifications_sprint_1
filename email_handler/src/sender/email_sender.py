import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

from core.config import get_settings

config = get_settings()


def send_message(email: str, content: str) -> None:
    """Функция для отправки сообщения через сервис транзакционной рассылки
    SendGrid

    Args:
        email(str): Email, на который необходимо отправки
        content(str): Шаблон HTML с содержанием сообщения
    """

    sg = sendgrid.SendGridAPIClient(api_key=config.sendgrid_api_key)
    from_email = Email(config.email_from)
    to_email = To(email)
    subject = "Новое сообщение от Practix"
    content = Content("text/html", content)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    sg.client.mail.send.post(request_body=mail_json)
