#! /usr/bin/env python3
# ~*~ utf-8 ~*~

import mailbox
import bs4
import json
import re


def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
    except AttributeError:  # message contents empty
        return None


class GmailMboxMessage:
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data

    def parse_email(self):
        # email_labels = self.email_data['X-Gmail-Labels']
        # email_date = self.email_data['Date']
        email_from = self.email_data['From']
        # email_to = self.email_data['To']
        # email_subject = self.email_data['Subject']
        email_text = self.read_email_payload()

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list, tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get('Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return (content_type, encoding, msg_text)


mbox_obj = mailbox.mbox('UN.mbox')
num_entries = len(mbox_obj)
pattern = re.compile(r'(href=".*?)[uU]nsubscribe')
sender_dict = {}
# load all emls with aspose

import aspose.email as ae
from aspose.email import MailMessage, SaveOptions, HtmlFormatOptions

# Load EML message
eml = MailMessage.load("Message.eml")

# Set SaveOptions
options = SaveOptions.default_html
options.embed_resources = False
options.HtmlFormatOptions = HtmlFormatOptions.WriteHeader | HtmlFormatOptions.WriteCompleteEmailAddress #save the message headers to output HTML using the formatting options

# Convert EML to HTML
eml.save("SaveAsHTML.html", options)


# save as html with aspose
# parse html with html parser
# get sender out and store as index
# search for re match and store as content
# print dict out to a file with json indent = 4


for idx, email_obj in enumerate(mbox_obj):
    email_data = GmailMboxMessage(email_obj)
    email_data.parse_email()
    sender = email_data.email_data["From"]
    if sender not in sender_dict:
        sender_dict[sender] = ""
    print((pattern.search(str(email_data.email_data)).group(1)))
    with open("text.txt", "w") as f:
        f.write(str(email_data.email_data))
        # f.write(pattern.search(str(email_data.email_data)).group(1).replace("\n", ""))
    print('Parsing email {0} of {1}'.format(idx, num_entries))