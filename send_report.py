import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f = open("orders_list.txt", 'r',  encoding="utf-8")

sender_email = "davidwuacc2@gmail.com"
sender_password = "qqyoseewqoazxexx"
recipient_email = "davidsiweiwu@gmail.com"
subject = "Daily Delivery Report"

body = f.read()


with open("orders_list.txt", "rb") as attachment:
    # Add the attachment to the message
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= 'attachment.txt'",
)

message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email
html_part = MIMEText(body)
message.attach(html_part)
message.attach(part)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, recipient_email, message.as_string())