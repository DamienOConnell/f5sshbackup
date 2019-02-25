#!/usr/bin/env python3

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = "user@gmail.com"
PASSWORD = "nopassword"


def get_contacts(filename):
    first = True
    emails = ""
    with open(filename, mode="r", encoding="utf-8") as contacts_file:
        for a_contact in contacts_file:
            if first:
                emails = emails + a_contact.strip()
                first = False
            else:
                emails = emails + "," + a_contact.strip()

    emails = str(emails)
    return emails


def read_template(filename):

    with open(filename, "r", encoding="utf-8") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_error_message(address_file, msg_template_file, subject_string, errormessage):

    emails = get_contacts(address_file)
    message_template = read_template(msg_template_file)  # read the message

    s = smtplib.SMTP(host="localhost", port=25)

    # print (emails)
    # print (str(emails))

    msg = MIMEMultipart()

    # template substitution
    message = message_template.substitute(ERRORMESSAGE=errormessage)

    # print(message)

    msg["From"] = MY_ADDRESS
    msg["To"] = emails
    msg["Subject"] = subject_string

    msg.attach(MIMEText(message, "plain"))

    s.send_message(msg)
    del msg

    s.quit()


def send_mail_message(
    address_file,
    msg_template_file,
    subject_string,
    backup_filename,
    backup_md5,
    usedspace,
):

    emails = get_contacts(address_file)
    message_template = read_template(msg_template_file)  # read the message

    s = smtplib.SMTP(host="localhost", port=25)

    # print (emails)
    # print (str(emails))

    msg = MIMEMultipart()

    # template substitution
    message = message_template.substitute(
        BACKUP_FILENAME=backup_filename, BACKUP_MD5=backup_md5, USEDSPACE=usedspace
    )

    # print(message)

    msg["From"] = MY_ADDRESS
    msg["To"] = emails
    msg["Subject"] = subject_string

    msg.attach(MIMEText(message, "plain"))

    s.send_message(msg)
    del msg

    s.quit()


def main():
    #
    send_mail_message(
        "contacts.txt",
        "msg_success.txt",
        "Fleet F5 backup success",
        "dummy_filename.tgz",
        "aef92bdf490",
        "50",
    )
    send_mail_message(
        "contacts.txt",
        "msg_failure.txt",
        "Fleet F5 backup failure",
        "dummy_filename.tgz",
        "aef92bdf490",
        "35",
    )


if __name__ == "__main__":
    main()
