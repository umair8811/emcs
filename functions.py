from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_Password_check(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password) 

def hashing_pass(password :str):
    return pwd_context.hash(password)

def send_verification_email(email: str, token: str):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_app_password"  # Replace with your app-specific password
    verification_link = f"http://yourdomain.com/verify?token={token}"  # Replace with your domain

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Verify Your Email Address"

    body = f"Please verify your email by clicking the following link: {verification_link}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")