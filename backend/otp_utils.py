from flask_mail import Message

# Generate a 6-digit OTP
def generate_otp():
    return '123456'

# Send OTP via email using Flask-Mail
def send_otp_email(recipient_email, otp):
    try:
        from app import mail, app  # Import mail and app from app to avoid circular import
        subject = 'Your Monsoon Days OTP'
        body = f'Your OTP for registration is: {otp}'

        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
        msg.body = body

        mail.send(msg)
        return True
    except Exception as e:
        print('Failed to send OTP:', e)
        return False
