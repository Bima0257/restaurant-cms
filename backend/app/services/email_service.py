import httpx

from app.config import settings


def send_otp_email(to_email: str, otp_code: str, full_name: str) -> bool:
    if not settings.RESEND_API_KEY:
        return False

    subject = f"Your verification code for WorldPlate"

    html_content = f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; background: #f4f4f4; margin: 0; padding: 0;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background: #f4f4f4;">
    <tr>
      <td align="center" style="padding: 40px 16px;">
        <table role="presentation" width="480" cellpadding="0" cellspacing="0" style="max-width: 480px; width: 100%%;">
          <tr>
            <td style="background: #e85d04; padding: 24px; text-align: center; border-radius: 12px 12px 0 0;">
              <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 800;">WorldPlate</h1>
            </td>
          </tr>
          <tr>
            <td style="background: #ffffff; padding: 40px 32px;">
              <p style="margin: 0 0 16px; color: #1a1a1a; font-size: 16px; line-height: 1.5;">Hi {full_name},</p>
              <p style="margin: 0 0 8px; color: #555; font-size: 14px; line-height: 1.6;">
                Thanks for creating an account with WorldPlate! To finish setting up your account, please verify your email address by entering the code below:
              </p>
              <div style="text-align: center; margin: 32px 0;">
                <span style="display: inline-block; font-size: 36px; font-weight: 700; letter-spacing: 8px; color: #e85d04; background: #fff5eb; padding: 16px 32px; border-radius: 8px;">{otp_code}</span>
              </div>
              <p style="margin: 0 0 4px; color: #888; font-size: 13px; text-align: center;">
                This code is valid for the next {settings.OTP_EXPIRE_MINUTES} minutes.
              </p>
              <p style="margin: 0; color: #888; font-size: 13px; text-align: center;">
                If you did not sign up for a WorldPlate account, you can safely ignore this email.
              </p>
            </td>
          </tr>
          <tr>
            <td style="background: #fafafa; padding: 20px 32px; text-align: center; border-top: 1px solid #eee; border-radius: 0 0 12px 12px;">
              <p style="margin: 0; font-size: 12px; color: #aaa;">&copy; 2026 WorldPlate. All rights reserved.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    text_content = f"""\
Hi {full_name},

Thanks for creating an account with WorldPlate! To finish setting up your account, please verify your email address by entering the code below:

{otp_code}

This code is valid for the next {settings.OTP_EXPIRE_MINUTES} minutes.

If you did not sign up for a WorldPlate account, you can safely ignore this email.

(c) 2026 WorldPlate. All rights reserved."""

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": "WorldPlate <noreply@leondev.web.id>",
                    "reply_to": "WorldPlate <noreply@leondev.web.id>",
                    "to": [to_email],
                    "subject": subject,
                    "html": html_content,
                    "text": text_content,
                },
            )
            return resp.is_success
    except Exception:
        return False
