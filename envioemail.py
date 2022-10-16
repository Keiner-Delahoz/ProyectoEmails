import smtplib
from email.message import EmailMessage

def enviar(email_destino,asunto,mensaje):
    email_origen="dnperez@uninorte.edu.co"
    password="morales101105"
    email= EmailMessage()
    email["From"] = email_origen
    email["To"] = email_destino
    email["Subject"] = asunto
    email.set_content(mensaje)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(email_origen,password)
    smtp.sendmail(email_origen,email_destino,email.as_string())
    smtp.quit()
