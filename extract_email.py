import imaplib
import email
import os
from dotenv import load_dotenv
import constants as CONSTANTS
from extract_pdf import extract_text
load_dotenv()


def download_attachement():
    mail = imaplib.IMAP4_SSL(os.getenv("gmail_host"))
    mail.login(os.getenv("email"), os.getenv("app_password"))
    mail.select("INBOX")

    current_dir = os. getcwd()
    if CONSTANTS.PDF_DIR not in os.listdir(current_dir):
        os.mkdir(CONSTANTS.PDF_DIR)

    _, selected_mails = mail.search(None, '(FROM "nadarmadhan43@gmail.com")',
                                    '(UNSEEN)')
    for num in selected_mails[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        _, bytes_data = data[0]
        email_message = email.message_from_bytes(bytes_data)
        for part in email_message.walk():
            if (part.get_content_type() == "text/plain" or
                    part.get_content_type() == "text/html"):
                message = part.get_payload(decode=True)
                print("Message: \n", message.decode())
            fileName = part.get_filename()

        if (bool(fileName)):
            filePath = os.path.join(current_dir, CONSTANTS.PDF_DIR, fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
    
if __name__ == "__main__":
    print("Job Started")
    try:
        download_attachement()
        print(extract_text())
    except Exception as e:
        print("Something went wrong!!")
    print("Job Completed")
