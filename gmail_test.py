#!/usr/bin/env python3
"""
Gmail Email Test Script
Tests email sending using Gmail SMTP with app password.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_gmail_test():
    """Send a test email using Gmail SMTP."""

    # Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    recipient_email = "shans.joe@gmail.com"

    print("Gmail Email Test")
    print("=" * 30)
    print()

    print("To use Gmail for sending emails:")
    print("1. Enable 2-Factor Authentication on your Gmail account")
    print("2. Generate an App Password:")
    print("   - Go to: https://myaccount.google.com/security")
    print("   - Click '2-Step Verification'")
    print("   - Scroll down to 'App passwords'")
    print("   - Generate a new app password for 'Mail'")
    print("   - Copy the 16-character password (like: abcd efgh ijkl mnop)")
    print()

    sender_email = input("Your Gmail address: ").strip()
    app_password = input("Gmail app password (16 characters): ").strip()

    if not sender_email or not app_password:
        print("❌ Gmail address and app password are required.")
        return

    # Create test message
    test_message = """
Subject: Test Email from Gradescope Analyzer 🧪

Hi Joe!

This is a test email from the Gradescope Analysis and Email System.

If you're receiving this email, it means the Gmail SMTP configuration is working correctly! 

The system is ready to send personalized emails to students based on their performance.

Best regards,
Gradescope Analyzer Test System
"""

    try:
        # Parse subject and body
        lines = test_message.strip().split("\n")
        subject = lines[0].replace("Subject: ", "")
        body = "\n".join(lines[1:]).strip()

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send email
        print(f"\nSending test email to {recipient_email}...")
        print(f"Using {smtp_server}:{smtp_port}")
        print(f"From: {sender_email}")

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        print("✅ Test email sent successfully!")
        print(f"Check {recipient_email} for the test message.")
        print("\n🎉 Gmail configuration is working!")
        print("You can now use this Gmail account to send emails to students.")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Please check your Gmail and app password.")
        print(
            "Make sure you're using the app password, not your regular Gmail password."
        )
        print("Also ensure 2FA is enabled on your Gmail account.")
    except smtplib.SMTPConnectError:
        print(
            "❌ Could not connect to Gmail SMTP server. Check your internet connection."
        )
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    send_gmail_test()
