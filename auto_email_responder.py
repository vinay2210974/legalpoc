from flask import Flask
import imaplib
import email
import smtplib
import schedule
import time

app = Flask(__name__)
print("Enter your Mail ID (MAKE SURE IT IS CORRECT)")
email_id = input()
print("Enter your app password")
password = input()
print("Thanks for credentials")

def generate_response(body):
    response_text = f"Thank you for your email. Your message '{body}' has been received and will be processed."
    return response_text

def read_emails(email_id, password):
    print('Checking for new emails...')
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_id, password)
    mail.select('inbox')

    # Search for unseen emails
    result, data = mail.search(None, 'UNSEEN')

    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract sender's email address
        sender = msg['From']

        # Parse email content
        subject = msg['Subject']
        body = ''
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode()

        # Check if sender email address contains 'noreply'
        if 'noreply' in sender:
            print(f"Skipping response for email from '{sender}' (contains 'noreply')")
            continue

        # Generate response
        response_text = generate_response(body)

        # Send response to the sender
        send_email(email_id, password, sender, 'Re: ' + subject, response_text)

    mail.close()
    mail.logout()

def send_email(email_id, password, to, subject, body):
    print(f'Sending email to {to} with subject "{subject}"')
    # Connect to SMTP server
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(email_id, password)

    # Compose email
    msg = f"Subject: {subject}\n\n{body}"

    # Encode message using UTF-8
    msg = msg.encode('utf-8')

    # Send email
    smtp_server.sendmail(email_id, to, msg)
    smtp_server.quit()

# Schedule email reading every 5 minutes
schedule.every(1).minutes.do(read_emails, email_id, password)

@app.route('/')
def index():
    return "Flask App is running!"

if __name__ == '__main__':
    while True:
        print('running')
        schedule.run_pending()
        time.sleep(1)
    app.run(debug=True)  # Run Flask app
