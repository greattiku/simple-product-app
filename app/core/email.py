import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.email import conf


load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
)



async def send_reset_email(
    email: str,
    token: str,
):
    reset_link = (
        f"{os.getenv('FRONTEND_URL')}"
        f"/reset-password?token={token}"
    )

#     message = MessageSchema(
#         subject="Reset Password",
#         recipients=[email],
#         body=f"""
# Click the link below to reset your password.

# {reset_link}

# If you didn't request this, ignore this email.
# """,
#         subtype=MessageType.plain,
#     )---> if youre using link to send the token
    message = MessageSchema(
        subject="Reset Password",
        recipients=[email],
        body=f"""
Hello,

You requested to reset your password.

Use the token below to reset your password:

{token}

This token expires in 15 minutes.

If you did not request this, please ignore this email.
""",
        subtype=MessageType.plain,
    )
    fm = FastMail(conf)

    await fm.send_message(message)