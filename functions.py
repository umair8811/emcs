from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_Password_check(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password) 

def hashing_pass(password :str):
    return pwd_context.hash(password)



def send_email(to_email, code):
    from_email = "mohammadumair1412@gmail.com"
    password = "ttwi clhq tzsh lkxv"  # Use App Password from Gmail

    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)