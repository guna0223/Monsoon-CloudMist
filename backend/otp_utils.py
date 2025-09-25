import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP via email
def send_otp_email(recipient_email, otp):
    sender_email = 'your_email@gmail.com'  # Replace with your email
    sender_password = 'your_password'      # Replace with your password
    subject = 'Your Monsoon Days OTP'
    body = f'Your OTP for registration is: {otp}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print('Failed to send OTP:', e)
        return False
