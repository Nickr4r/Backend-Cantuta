import os
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER = os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def enviar_correo_recuperacion(email: str, token: str):
    fastmail = FastMail(conf)
    
    # Enlace que el usuario verá en su correo
    base_url = os.getenv("FRONTEND_URL")
    url_reset = f"{base_url}/login/restablecer-password?token={token}"
    
    # Diseño del correo en HTML
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px;">
        <h2 style="color: #1a237e; text-align: center;">Recuperación de Contraseña</h2>
        <p>Hola,</p>
        <p>Has solicitado restablecer tu contraseña en el <b>Sistema La Cantuta</b>. Haz clic en el botón de abajo para continuar:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{url_reset}" style="background-color: #00e5b0; color: #0b2b24; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                RESTABLECER MI CONTRASEÑA
            </a>
        </div>
        <p style="color: #666; font-size: 12px;">Este enlace es válido por 15 minutos. Si no solicitaste este cambio, puedes ignorar este mensaje de forma segura.</p>
        <hr style="border: 0; border-top: 1px solid #eee;">
        <p style="text-align: center; color: #999; font-size: 10px;">Sistema de Gestión Académica La Cantuta - 2024</p>
    </div>
    """

    message = MessageSchema(
        subject="Recuperación de Contraseña - La Cantuta",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    await fastmail.send_message(message)