import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SMTP_HOST = "localhost" #smpt.runbox.com
SMTP_PORT = 25 #587
SMTP_USER = ""
SMTP_PASS = ""
FROM_ADDR = "noreply@quiongos.pi"
TO_ADDR = ["jose.pereira@aptoide.com", "zepcp@hotmail.com"]

def send_email(subject, message, from_addr, to_addr,
              smtp_host, smtp_port, smtp_user, smtp_pass,
              attachments=[], html=False):

    # Create a text/plain message
    msg = MIMEMultipart("mixed")

    msg["Subject"] = subject
    msg["To"] = ",".join(to_addr)
    msg.attach(MIMEText(message, "html" if html else "plain"))

    for f in attachments:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(fil.read(),
                                       Content_Disposition = 'attachment; filename="%s"' % f,
                                       Name = f))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    if smtp_user:
        server.login(smtp_user, smtp_pass)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

if __name__ == "__main__":
    mail_subject = "KPI Migrator"
    mail_body = 'Migrator Stats For Yesterday'

    send_email(mail_subject, mail_body,
               FROM_ADDR, TO_ADDR,
               SMTP_HOST, SMTP_PORT, 
               SMTP_USER, SMTP_PASS)
