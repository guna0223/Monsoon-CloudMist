import random
from flask_mail import Message

# Generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP via email using Flask-Mail
def send_otp_email(recipient_email, otp):
    from app import mail  # Import mail from app
    subject = 'Your Monsoon Days OTP'
    body = f'Your OTP for registration is: {otp}'

    msg = Message(subject, sender='your_email@gmail.com', recipients=[recipient_email])
    msg.body = body

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print('Failed to send OTP:', e)
        return False
