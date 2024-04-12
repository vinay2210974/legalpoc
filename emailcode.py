import imaplib
import smtplib
import email
import logging
import schedule
import time
# Configure logging
logging.basicConfig(filename='email_integration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_response(body):
    response_text = f"Testing my project - Ignore - Thank you for your email. Your message '{body}' has been received and will be processed."
    return response_text
def read_emails():
    logging.info('Checking for new emails...')
    print('checking')
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    print('login')
    mail.login('sujatha.informategy@gmail.com', 'cmvt wpef ozpg bmuu')
    mail.select('inbox')

    # Search for unseen emails
    result, data = mail.search(None, 'UNSEEN')
    print('fetching')
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
            logging.info(f"Skipping response for email from '{sender}' (contains 'noreply')")
            continue

        # Generate response
        response_text = generate_response(body)
        print('sending mail')
        # Send response to the sender
        send_email(sender, 'Re: ' + subject, response_text)

    mail.close()
    mail.logout()


def send_email(to, subject, body):
    logging.info(f'Sending email to {to} with subject "{subject}"')
    # Connect to SMTP server
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login('sujatha.informategy@gmail.com', 'cmvt wpef ozpg bmuu')

    # Compose email
    msg = f"Subject: {subject}\n\n{body}"

    # Encode message using UTF-8
    msg = msg.encode('utf-8')
    print('almost done')
    # Send email
    smtp_server.sendmail('sujatha.informategy@gmail.com', to, msg)
    smtp_server.quit()


# Schedule email reading every 1 minute
schedule.every(1).minutes.do(read_emails)

while True:
    logging.info('Script is running...')
    print('running')
    schedule.run_pending()
    time.sleep(1)
