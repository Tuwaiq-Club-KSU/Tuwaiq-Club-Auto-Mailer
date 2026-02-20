import argparse
import csv
import smtplib
import ssl
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_emails(csv_path, template_path, role, subject, sender_name, name_col, track_col, email_col):
    # Get credentials and config
    sender_email = os.getenv("CLUB_EMAIL")
    password = os.getenv("CLUB_EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not sender_email or not password:
        print("Error: CLUB_EMAIL or CLUB_EMAIL_PASSWORD not set in .env file.")
        sys.exit(1)

    # Read Template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)

    # Connect to SMTP Server
    server = None
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)
        server.login(sender_email, password)
        print(f"Successfully connected to {smtp_server} as {sender_email}")
    except Exception as e:
        print(f"Error connecting to SMTP server: {e}")
        sys.exit(1)

    # Read CSV and Send Emails
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f: # utf-8-sig handles BOM if present
            reader = csv.DictReader(f)
            
            # Verify columns exist
            if reader.fieldnames:
                missing_cols = []
                if name_col not in reader.fieldnames: missing_cols.append(name_col)
                if track_col not in reader.fieldnames: missing_cols.append(track_col)
                if email_col not in reader.fieldnames: missing_cols.append(email_col)
                
                if missing_cols:
                    print(f"Error: The following columns were not found in the CSV: {', '.join(missing_cols)}")
                    print(f"Available columns: {', '.join(reader.fieldnames)}")
                    sys.exit(1)

            count = 0
            for row in reader:
                name = row.get(name_col, "").strip()
                track = row.get(track_col, "").strip()
                recipient_email = row.get(email_col, "").strip()

                if not recipient_email:
                    print(f"Skipping row with missing email: {row}")
                    continue

                # Prepare Email Content
                body = (template_content.replace("{{NAME}}", name)
                                       .replace("{{TRACK}}", track)
                                       .replace("{{ROLE}}", role))

                msg = MIMEMultipart()
                msg['From'] = f"{sender_name} <{sender_email}>"
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))

                # Send
                try:
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    print(f"Sent email to: {name} ({recipient_email})")
                    count += 1
                except Exception as e:
                    print(f"Failed to send to {recipient_email}: {e}")

            print(f"
Finished! Sent {count} emails.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if server:
            server.quit()

def main():
    parser = argparse.ArgumentParser(description="Tuwaiq Auto Mailer - A CLI tool for sending automated club emails.")
    
    parser.add_argument("-c", "--csv", required=True, help="Path to the CSV file containing recipient data")
    parser.add_argument("-t", "--template", required=True, help="Path to the HTML template file")
    parser.add_argument("-r", "--role", required=True, help="The role to assign (e.g., 'عضو', 'قائد')")
    parser.add_argument("-s", "--subject", required=True, help="Email subject line")
    parser.add_argument("-n", "--name", required=True, help="Sender name (e.g., 'Tuwaiq Club')")
    
    # Optional column overrides with defaults
    parser.add_argument("--name-col", default="Name", help="Column name for recipient's name (default: 'Name')")
    parser.add_argument("--track-col", default="Track", help="Column name for recipient's track/department (default: 'Track')")
    parser.add_argument("--email-col", default="Email", help="Column name for recipient's email (default: 'Email')")

    args = parser.parse_args()

    send_emails(
        args.csv, 
        args.template, 
        args.role, 
        args.subject, 
        args.name,
        args.name_col, 
        args.track_col, 
        args.email_col
    )

if __name__ == "__main__":
    main()
