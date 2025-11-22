import os
import smtplib
from flask import Flask, jsonify
from email.message import EmailMessage

app = Flask(__name__)

# Get environment variables (set these in Vercel or local shell)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TEST_MAIL = os.getenv("TEST_MAIL")
FROM_NAME = os.getenv("FROM_NAME", "Flask Mailer")

ATTACHMENT_PATH = "sample_media.txt"


def create_sample_media():
    """Creates a text file to attach, if it doesn’t already exist."""
    if not os.path.exists(ATTACHMENT_PATH):
        with open(ATTACHMENT_PATH, "w", encoding="utf-8") as f:
            f.write(
                "Sample Media File\n"
                "------------------\n"
                "This is an auto-generated file used only for testing mail attachment.\n"
                "No personal images or user-provided media.\n"
            )


def send_test_email():
    # Ensure sample attachment exists
    create_sample_media()

    msg = EmailMessage()
    msg["Subject"] = "Flask Test Email (SMTP 587)"
    msg["From"] = f"{FROM_NAME} <{SMTP_USER}>"
    msg["To"] = TEST_MAIL

    msg.set_content(
        "Hello,\n\n"
        "This is a test email sent using Flask + SMTP on port 587.\n"
        "A sample generated attachment is included.\n\n"
        "Regards,\nFlask Mailer\n"
    )

    # Add attachment
    with open(ATTACHMENT_PATH, "rb") as f:
        file_data = f.read()
    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=ATTACHMENT_PATH,
    )

    # SMTP send
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    return True


@app.route("/", methods=["GET"])
def send_mail_route():
    try:
        send_test_email()
        return jsonify({"status": "success", "message": "Mail sent!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=12000)
