import asyncio
import websockets
import smtplib
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError

# — SMTP Configuration (fill these) —
SMTP_HOST    = "smtp.gmail.com"
SMTP_PORT    = 587
SMTP_USER    = "tutaahmed.f@gmail.com"            # ← CHANGE THIS
SMTP_PASS    = "knrn saai potc zoel"  # ← CHANGE THIS
FROM_ADDRESS = SMTP_USER
# ——————————————————————————————

def send_email(to_address: str) -> bool:
    """Send the “hi” email; return True if send() didn't raise."""
    msg = EmailMessage()
    msg["From"]    = FROM_ADDRESS
    msg["To"]      = to_address
    msg["Subject"] = "Hello!"
    msg.set_content("hi")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
    return True

async def handler(ws):
    async for message in ws:
        try:
            # 1) Validate format & check MX record
            v = validate_email(message, check_deliverability=True)
            email = v.email  # normalized

        except EmailNotValidError:
            # invalid format or no MX records
            await ws.send("⚠️ Couldn’t find you.")
            continue

        # 2) Attempt to send
        try:
            send_email(email)
        except Exception:
            await ws.send("❌ Failed to send email.")
        else:
            await ws.send("✅ I have just texted you.")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())


