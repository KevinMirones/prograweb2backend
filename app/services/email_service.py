import os
import asyncio
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

# Configuration with increased timeout and proper SSL settings
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")  # MUST be App Password for Gmail
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)

# Critical: Use SSL on port 465 instead of STARTTLS on 587
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=465,  # Changed from 587 to 465
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,  # Disabled for SSL
    MAIL_SSL_TLS=True,  # Enabled for SSL
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TIMEOUT=30,  # Increased timeout
    MAIL_DEBUG=1  # Enable debugging
)

async def send_mfa_code(email: EmailStr, code: str):
    """
    Send MFA code with timeout handling
    """
    html = f"""
    <p>Your verification code is: <strong>{code}</strong></p>
    <p>This code will expire in 10 minutes.</p>
    """
    
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    
    try:
        # Add timeout to prevent hanging
        await asyncio.wait_for(fm.send_message(message), timeout=30)
        print(f"✅ Email sent successfully to {email}")
        return True
    except asyncio.TimeoutError:
        print("❌ Email sending timed out after 30 seconds")
        # Fallback to console output for debugging
        print(f"📧 [FALLBACK] MFA Code for {email}: {code}")
        return False
    except Exception as e:
        print(f"❌ Failed to send email to {email}: {str(e)}")
        # Fallback to console output
        print(f"📧 [FALLBACK] MFA Code for {email}: {code}")
        return False