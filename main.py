import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PWD = os.getenv("EMAIL_PWD")

def send_email():
    msg = MIMEText("Hola! Esto es un Hello World automático desde GitHub Actions 🚀")
    msg["Subject"] = "Hello World - Ejecución automática"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER  # puedes enviar a ti mismo

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PWD)
        server.send_message(msg)


if __name__ == "__main__":
    print("Ejecutando script: Hello World!")
    send_email()
