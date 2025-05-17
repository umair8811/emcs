from passlib.context import CryptContext
from dotenv import load_dotenv
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_Password_check(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password) 

def hashing_pass(password :str):
    return pwd_context.hash(password)



SENDER_EMAIL = "mohammadumair1412@gmail.com"
SENDER_PASSWORD = "bqaa cznb rqnx oifv"  # Your Gmail app password
BASE_URL = "http://16.171.1.109:8000"

def send_verification_email(email: str, token: str):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValueError("Invalid email address")

    verification_link = f"{BASE_URL}/verify?token={token}"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = "Verify Your Email Address"

    body = f"""
Hello,

Please verify your email address by clicking the link below:

{verification_link}

This link will expire in 24 hours.

Best regards,
Event Management Team
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.set_debuglevel(1)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email sending error:", e)
        raise RuntimeError(f"Failed to send email: {str(e)}")
    