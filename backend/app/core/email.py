import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.core.config import settings

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def get_base_template(content: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: #f9fafb;
                margin: 0;
                padding: 0;
                -webkit-font-smoothing: antialiased;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 4px 25px rgba(0, 0, 0, 0.05);
            }}
            .header {{
                padding: 40px 40px 20px;
                text-align: center;
            }}
            .logo {{
                font-size: 24px;
                font-weight: 800;
                color: #111111;
                text-decoration: none;
                letter-spacing: -0.02em;
            }}
            .content {{
                padding: 20px 40px;
                color: #374151;
                line-height: 1.6;
            }}
            .footer {{
                padding: 30px 40px 40px;
                text-align: center;
                font-size: 13px;
                color: #9ca3af;
                background-color: #fafafa;
            }}
            .button {{
                display: inline-block;
                padding: 16px 32px;
                background-color: #111111;
                color: #ffffff !important;
                text-decoration: none;
                border-radius: 14px;
                font-weight: 700;
                margin-top: 20px;
                transition: transform 0.2s;
            }}
            .code-box {{
                background-color: #f3f4f6;
                padding: 24px;
                border-radius: 16px;
                text-align: center;
                margin: 24px 0;
            }}
            .code {{
                font-size: 32px;
                font-weight: 800;
                letter-spacing: 0.2em;
                color: #111111;
                margin: 0;
            }}
            h2 {{
                color: #111111;
                font-size: 24px;
                font-weight: 800;
                margin-top: 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">STORELY</div>
            </div>
            <div class="content">
                {content}
            </div>
            <div class="footer">
                &copy; {datetime.now().year} Storely. All rights reserved.<br>
                Empowering your digital commerce.
            </div>
        </div>
    </body>
    </html>
    """

def send_verification_code(email: str, code: str):
    subject = "Verify your email - Storely"
    content = f"""
        <h2>Verify your email</h2>
        <p>Welcome to Storely! Use the code below to complete your registration and secure your account.</p>
        <div class="code-box">
            <div class="code">{code}</div>
        </div>
        <p>This code will expire in <strong>15 minutes</strong> for security reasons. If you didn't request this code, you can safely ignore this email.</p>
    """
    body = get_base_template(content)
    return send_email(email, subject, body)

def send_password_reset_email(email: str, token: str):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    subject = "Reset your password - Storely"
    content = f"""
        <h2>Reset your password</h2>
        <p>We received a request to reset your Storely password. No problem, it happens to the best of us!</p>
        <p>Click the button below to choose a new password:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_url}" class="button">Reset Password</a>
        </div>
        <p>This link will expire in 1 hour. If you didn't request this, your account is still secure and you can ignore this email.</p>
    """
    body = get_base_template(content)
    return send_email(email, subject, body)
