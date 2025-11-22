from flask import Flask, request, jsonify
import os, smtplib, base64
from email.message import EmailMessage

app = Flask(__name__)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_NAME = os.getenv("FROM_NAME", "Mailer Service")


@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.json
        email = data["email"]
        filename = data["filename"]
        filedata_b64 = data["filedata"]

        # decode base64 → PDF bytes
        file_bytes = base64.b64decode(filedata_b64)

        msg = EmailMessage()
        msg["Subject"] = "Your Expense Report"
        msg["From"] = f"{FROM_NAME} <{SMTP_USER}>"
        msg["To"] = email

        msg.set_content("Attached is your expense report.")

        msg.add_attachment(
            file_bytes,
            maintype="application",
            subtype="pdf",
            filename=filename
        )

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=12000)
