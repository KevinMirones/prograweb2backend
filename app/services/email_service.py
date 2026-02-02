import asyncio
import os
import aiohttp
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_mfa_code(email: str, code: str) -> bool:
    """
    Send MFA code using Resend API (works on Render)
    """
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    
    if not RESEND_API_KEY:
        logger.error(" RESEND_API_KEY not set in environment variables")
        logger.info(f" [FALLBACK] MFA Code for {email}: {code}")
        return False
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Your sender email (you'll need to verify it in Resend dashboard first)
    # For testing, use the default Resend email
    sender_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    
    data = {
        "from": sender_email,
        "to": [email],
        "subject": "Tu código de verificación",
        "html": f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0; color: white;">
                <h1 style="margin: 0;">Código de Verificación</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; border: 1px solid #e0e0e0;">
                <p>Hola,</p>
                <p>Tu código de verificación es:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <div style="font-size: 32px; font-weight: bold; letter-spacing: 10px; color: #667eea; padding: 20px; background: white; border-radius: 8px; display: inline-block; border: 2px dashed #667eea;">
                        {code}
                    </div>
                </div>
                <p>Este código expirará en <strong>10 minutos</strong>.</p>
                <p>Si no solicitaste este código, ignora este correo.</p>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">
                    Este es un mensaje automático, por favor no respondas a este correo.
                </p>
            </div>
        </div>
        """
    }
    
    try:
        logger.info(f" Sending MFA code to {email} via Resend API")
        logger.info(f" Code: {code}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f" Email sent successfully via Resend. ID: {result.get('id')}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f" Resend API error: {response.status} - {error_text}")
                    logger.info(f" [FALLBACK] MFA Code for {email}: {code}")
                    return False
                    
    except asyncio.TimeoutError:
        logger.error(" Resend API timeout after 10 seconds")
        logger.info(f"[FALLBACK] MFA Code for {email}: {code}")
        return False
    except Exception as e:
        logger.error(f" Exception sending email via Resend: {str(e)}")
        logger.info(f" [FALLBACK] MFA Code for {email}: {code}")
        return False