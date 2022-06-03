import imaplib
import json
import os
import re
from datetime import datetime, timedelta
import email
import time
from bs4 import BeautifulSoup


def get_gmail_data():
    json_file = f"{os.path.dirname(__file__)}/gmail_info/client_secret.json"
    with open(json_file) as gmail_info:
        data = json.load(gmail_info)
    return data


GMAIL_DATA = get_gmail_data()

EMAIL = GMAIL_DATA['email']
USERNAME = GMAIL_DATA['username']
PASSWORD = GMAIL_DATA['password']

"""http://www.marshallsoft.com/ImapSearch.htm contains a list of search syntax for IMAP"""

"""Any tests retrieving an email from the server need to set a test_start_time at the beginning of the test
    this is the syntax for that: test_start_time = datetime.now().utcnow() """

# region Get Email Info

def confirm_email_recieved_by_subject(subject, test_start_time):

    """Waits for the email to show up"""

    mail = select_inbox()
    wait_for_email_by_email_subject(subject, test_start_time)
    mail.noop()
    most_recent_email_id = get_most_recent_mail_id_by_subject(subject)

    """Gets the content of the most recent email"""
    content = mail.fetch(most_recent_email_id, "RFC822.TEXT")

    """Creates the Message Object and parses the body"""
    msg = email.message_from_string(str(content[1]))

    """Returns a simple Email object"""
    return msg

def does_most_recent_email_contain_text(subject, body_string, test_start_time):

    """'body_string' is the text in the body of the email that you want to assert against"""

    """Waits for the email to show up"""
    mail = select_inbox()
    wait_for_email_by_email_subject(subject, test_start_time)
    mail.noop()
    most_recent_email_id = get_most_recent_mail_id_by_subject(subject)

    """Gets the content of the most recent email"""
    content = mail.fetch(most_recent_email_id, "RFC822.TEXT")

    """Creates the Message Object and parses the body"""
    msg = email.message_from_string(str(content[1]))
    parsed_response = parse_payload(msg)

    for x in parsed_response:
        if body_string in x:
            return True

def get_password_from_email(test_start_time):

    """This searches the inbox for the Password Reset emails, grabs the most recent one that was sent after
        the start of the test, and returns the password"""

    mail = select_inbox()
    wait_for_email_by_email_subject("password has been reset", test_start_time)
    mail.noop()
    most_recent_email_id = get_most_recent_mail_id_by_subject("password has been reset")
    content = mail.fetch(most_recent_email_id, "RFC822.TEXT")
    msg = email.message_from_string(str(content[1]))
    parsed_response = parse_payload(msg)
    for x in parsed_response:
        if "Your password has been reset to:" in x:
            password = x.split(": ")[1]
            break
    return password


def get_mfa_code_from_email(test_start_time):

    """This searches the inbox for the Multi-Factor Authentication emails, grabs the most recent one that was sent after
        the start of the test, and returns the code"""

    mail = select_inbox()
    wait_for_email_by_email_subject("Your authentication code.", test_start_time)
    mail.noop()
    most_recent_email_id = get_most_recent_mail_id_by_subject("Your authentication code.")
    content = mail.fetch(most_recent_email_id, "RFC822.TEXT")
    msg = email.message_from_string(str(content[1]))
    parsed_response = parse_payload(msg)
    for x in parsed_response:
        if "Your code for authentication is " in x:
            mfa_code = re.sub("[^0-9]", "", x.split(", ")[1])
            break
    return mfa_code

# endregion Get Email Info

# region Delete Emails

def delete_emails_by_subject(subject):

    """this will delete all emails in the inbox based on the subject you pass in"""

    mail = select_inbox()
    data = mail.search(None, f'SUBJECT "{subject}"')
    messages = data[1][0].split()
    for email in messages:
        mail.store(email, "+X-GM-LABELS", "\\Trash")
    mail.expunge()

def delete_all_emails_older_than_one_day():
    mail = select_inbox()
    data = mail.search(None, f'BEFORE "{((datetime.now().utcnow()) - timedelta(days=1)).strftime("%d-%b-%Y")}"')
    messages = data[1][0].split()
    for email in messages:
        mail.store(email, "+X-GM-LABELS", "\\Trash")
    mail.expunge()

# endregion Delete Emails


"""Below are Support Methods for the functional methods in this Module, these typically should not be called
    to the Page or Test layers and are just used on this page"""

# region Support Methods

def select_inbox():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    return mail

def get_most_recent_mail_id_by_subject(subject):

    """Pass in the subject you are searching for, this will wait for an email to hit the inbox
        that matches that subject if there currently are none"""

    count = 0
    mail = select_inbox()
    mail_search_object = mail.search(None, f'SUBJECT "{subject}"')
    ids = mail_search_object[1]
    mail_ids = ids[0].split()
    while not mail_ids and count <= 300:
        time.sleep(1); count+=1
        mail.noop()
        mail_search_object = mail.search(None, f'SUBJECT "{subject}"')
        ids = mail_search_object[1]
        mail_ids = ids[0].split()
        if count > 300:
            Exception("Email never showed up in the inbox")
    most_recent_email_id = mail_ids[-1]
    return most_recent_email_id

def wait_for_email_by_email_subject(subject, test_start_time):

    """This will wait for an email to hit the inbox after the start of the test and
        by the subject you search for"""

    count = 0
    mail = select_inbox()
    most_recent_email_id = get_most_recent_mail_id_by_subject(subject)
    mail.noop()
    timestamp = mail.fetch(most_recent_email_id, "INTERNALDATE")
    timestamp = (re.findall(r'"([^"]*)"', str(timestamp)))[0]
    timestamp = datetime.strptime(timestamp, "%d-%b-%Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")
    while str(test_start_time) > timestamp and count <= 300:
        time.sleep(1); count+=1;
        mail.noop()
        most_recent_email_id = get_most_recent_mail_id_by_subject(subject)
        timestamp = mail.fetch(most_recent_email_id, "INTERNALDATE")
        timestamp = (re.findall(r'"([^"]*)"', str(timestamp)))[0]
        timestamp = datetime.strptime(timestamp, "%d-%b-%Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")


# "message" needs to be an email message object. "var = email.get_message_from_string(var2)" as an example
def parse_payload(message):

    """Parses the payload of the message object """
    msg_array = []
    message.get_payload()
    for part in message.walk():
        if part.get_content_type():
            body = str(part.get_payload())
            soup = BeautifulSoup(body)
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                msg_array.append(paragraph.text)
    return msg_array

# endregion Support Methods