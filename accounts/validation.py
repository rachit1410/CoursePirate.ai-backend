import re
import smtplib
import dns.resolver


def email_validation(email):
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None:
        return False
    return True

def verify_email(email):
    domain = email.split('@')[1]

    # Step 1: Get MX Record for the domain
    try:
        records = dns.resolver.resolve(domain, 'MX')
        # Get the mail server with the highest priority (lowest preference number)
        mx_record = sorted(records, key=lambda record: record.preference)[0].exchange.to_text()
    except Exception as e:
        return False

    # Step 2: SMTP Handshake
    try:
        # Connect to the target SMTP server on standard port 25
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_record, 25)
        
        # Say hello to the server (use a generic or your actual domain)
        server.helo(server.local_hostname) 
        
        # Specify the sender address (required by the protocol)
        server.mail('test@example.com')
        
        # This is the crucial step: check if the recipient exists
        code, message = server.rcpt(email)
        
        # Always be nice and close the connection
        server.quit()

        # SMTP Code 250 means success / mailbox exists
        if code == 250:
            return True
        else:
            return False

    except Exception as e:
        return False

def password_validation(password):
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password) is None:
        return False
    return True
