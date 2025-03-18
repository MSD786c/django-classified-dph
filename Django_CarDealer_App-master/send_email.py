import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
username = 'dphtrial@gmail.com'
password = 'cqje yrqc foeb qzuk'

# Create the email components
sender_email = username
receiver_email = 'suhaylindubai@gmail.com'
subject = 'Test Email from Python'
body = 'This is a test email sent from a Python script using SMTP!'

# Create a multipart message and set headers
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Add body to email
message.attach(MIMEText(body, 'plain'))

# Create a secure SSL context
context = smtplib.SMTP_SSL('smtp.gmail.com', 465)

try:
    # Log in to server and send email
    context.login(username, password)
    context.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    context.quit()
