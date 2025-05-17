from passlib.context import CryptContext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_Password_check(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password) 

def hashing_pass(password :str):
    return pwd_context.hash(password)



# Function to send verification email
def send_verification_email(email: str, token: str):
    # Get credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
    sender_password = os.getenv("SENDER_PASSWORD", "your_app_password")
    base_url = os.getenv("BASE_URL", "http://16.171.1.109:8000")

    # Validate email format
    email_regex = r'^[a-zA-Z0-9]+([._%+-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,7}$'
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email address")

    verification_link = f"{base_url}/verify?token={token}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Verify Your Email Address"

    # Enhanced email body
    body = f"""
    Hello,

    Thank you for registering with Event Management. Please verify your email address by clicking the link below:

    {verification_link}

    This link will expire in 24 hours. If you did not request this, please ignore this email.

    Best regards,
    Event Management Team
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=500, detail="Failed to send email: Invalid sender credentials")
    except smtplib.SMTPRecipientsRefused:
        raise HTTPException(status_code=400, detail="Failed to send email: Invalid recipient email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")



# # Function to send verification email
# def send_verification_email(email: str, token: str):
#     sender_email = "your_email@gmail.com"           # ✅ Your Gmail address
#     sender_password = "your_app_password"           # ✅ Gmail App Password (not your normal password)

#     # ✅ Your actual FastAPI server IP and verification endpoint
#     verification_link = f"http://16.171.1.109:8000/verify?token={token}"

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = email
#     msg['Subject'] = "Verify Your Email Address"

#     body = f"Please verify your email by clicking the following link:\n{verification_link}"
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, email, msg.as_string())
#         server.quit()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
