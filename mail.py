import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_mail(raport):
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()

    login = 'yourfavouriterestaurant81@gmail.com'
    password = os.environ['MAIL_STR']
    smtp_object.login(login, password)

    mail = 'yourfavouriterestaurant81@gmail.com'
    subject = "Daily raport"

    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = mail
    msg['Subject'] = subject

    msg.attach(MIMEText(raport, 'plain'))

    try:
        smtp_object.send_message(msg)
        print("Wiadomość wysłana pomyślnie!")
    except Exception as e:
        print(f"Wysyłanie się nie powiodło! Błąd: {e}")
    finally:
        smtp_object.quit()

  