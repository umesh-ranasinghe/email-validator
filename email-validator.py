import re
import argparse
from email import policy
from email.parser import BytesParser

def validate_email_headers(email):
    # Check required headers
    required_headers = ['From', 'To', 'Date', 'Subject', 'Message-ID']
    for header in required_headers:
        if header not in email:
            return f"Missing required header: {header}"
    
    # Validate Date format
    date_pattern = r'\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} [-+]\d{4}'
    if not re.match(date_pattern, email['Date']):
        return "Invalid Date format"
    
    # Validate Message-ID format
    message_id_pattern = r'<.+@.+>'
    if not re.match(message_id_pattern, email['Message-ID']):
        return "Invalid Message-ID format"
    
    return "The email headers are valid."

def load_email_from_file(file_path):
    with open(file_path, 'rb') as f:
        email = BytesParser(policy=policy.default).parse(f)
    return email

def parse_input_arguments():
    parser = argparse.ArgumentParser(description="""This program checks an email for RFC5322 compliance.
                                     You may provide the email file path to the program when executing.""")
    parser.add_argument(
        "-f", "--filepath", required=True, help="Path of the email file."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_input_arguments()
    file_path = args.filepath
    email = load_email_from_file(file_path)
    result = validate_email_headers(email)
    print(result)

