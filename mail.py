import os
from dotenv import load_dotenv
from helpers.mail_helper import EmailHelper
load_dotenv()

EMAIL_API_TOKEN = os.getenv("EMAIL_API_TOKEN")
helper = EmailHelper(api_key=EMAIL_API_TOKEN)
inbox = helper.create_inbox()
print("Email:", inbox["email"])

# Отправь письмо на этот адрес
email = helper.wait_for_email(inbox["id"])
print("Тема:", email["subject"])
link = helper.get_link(email["body"])
print("Ссылка:", link)
helper.close()

