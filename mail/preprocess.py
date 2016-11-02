#!/usr/bin/env python

"""
Usage: %s input_file output_file [filter]

This Program extract all Message Bodies and Subject from an EMail mbox Archive

Encoded Mails (multipart/base64) are tried to be decoded.
This writes every email in its own line with spaces seperating the words

Filter is a string that must appear in one of the FILTER_HEADERS fields, otherwise the mail is skipped.
The Filter can be inverted by prepending a '!'
"""

import os
import sys
import re
import quopri
import base64
from gensim.corpora.textcorpus import TextCorpus
from mailbox import mbox
from HTMLParser import HTMLParser

FILTER_HEADERS = ['From', 'To']

class MLStripper(HTMLParser):
    #tokens that contain data but are no text
    IGNORETEAGS = set(['script', 'style'])

    def __init__(self):
        self.reset()
        self.fed = []
        self.tagStack = []

    def handle_data(self, d):
        if not len(MLStripper.IGNORETEAGS.intersection(set(self.tagStack))) > 0:
            self.fed.append(d)

    def handle_starttag(self, tag, attrs):
        self.tagStack.append(tag)

    def handle_endtag(self, tag):
        if len(self.tagStack) > 0:
            self.tagStack.pop()

    def get_data(self):
        return ''.join(self.fed)

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def extract_text(mail):
    payload = mail.get_payload()
    content = ''

    # if the message is multipart data, concatenate all parts
    if mail.is_multipart():
        for subMail in payload:
            part = extract_text(subMail)
            content += str(part)
    else:
        content = payload

    coding = mail['Content-Transfer-Encoding']
    if coding == 'quoted-printable':
        #decode mime coded printable strings
        content = quopri.decodestring(content)
    elif coding == 'base64':
        content = base64.b64decode(content)

    #check the content type for further processing
    content_type = mail.get_content_type()
    if content_type == 'text/plain':
        # dont need to transform the data
        pass
    elif content_type == 'text/html':
        #strip the html content
        content = strip_html(content)
    elif content_type == 'multipart/alternative':
        # we cant really do anything here
        # dont transform the file
        pass
    else:
        # another type, probably binary (images/pdf/...)
        # delete the binary content and ignore it
        content = ' '

    #normalize to lower case
    content = content.lower()

    # remove newlines
    content = content.replace('\n', ' ')
    content = content.replace('\r', ' ')
    content = content.replace('\t', ' ')

    #remove all urls and replace them with a fixed token
    content = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', content)

    #remove all "special characters"
    content = re.sub('\W', ' ', content, re.UNICODE)

    #remove all series of more than one spacer characters
    #because they are often used as horizontal lines
    content = re.sub('[-, _, \s, \*, \+, =, >, \.]+', ' ', content)
    #normalize white spaces
    content = re.sub(' +', ' ', content)

    content = content.decode('ISO-8859-2').encode('utf-8')
    return content


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print __doc__ % sys.argv[0].split("/")[-1]
        sys.exit(1)

    in_file, out_file_path = sys.argv[1:3]
    filter_address = sys.argv[3] if len(sys.argv) >= 4 else None
    filter_inverted = False

    if filter_address is not None:
        filter_inverted = filter_address[0] == '!'
        if filter_inverted:
            filter_address = filter_address[1:]
        print('filtering messages with filter {}'.format(filter_address))

    temp_file_path = out_file_path + '.temp'
    temp_file = open(temp_file_path, 'w')

    print('parsing input file ...')
    mailbox = mbox(in_file)

    parsed_messages = 0
    unparseable_messages = 0
    filtered_messages = 0

    for mail in mailbox:
        sys.stdout.write("parsed {} messages, skipped {}\r".format(parsed_messages, filtered_messages))

        if filter_address is not None:
            #print any([filter_address in mail[field].join(' ') for field in FILTER_HEADERS if mail[field] is not None])

            filter_matches = any([filter_address in str(mail[field]) for field in FILTER_HEADERS if mail[field] is not None])
            filter_matches = filter_matches ^ filter_inverted
            if not filter_matches:
                #skip this entry as is does not statisfy the filter
                filtered_messages += 1
                continue

        try:
            content = extract_text(mail)
            parsed_messages += 1
        except:
            content = ''
            unparseable_messages += 1

        temp_file.write(content + '\n')

    temp_file.close()

    print('encountered {} unparseable messages'.format(unparseable_messages))
    print('parsed {} messages'.format(parsed_messages))
    print('skipped {} messages'.format(filtered_messages))

    print('generating Gensim corpus')

    out_file = open(out_file_path, 'w')
    corpus = TextCorpus(temp_file_path)
    print('corpus generated, saving to disk')
    saved_messages = 0

    for text in corpus.get_texts():
        line = " ".join(text) + "\n"
        out_file.write(line.encode('utf-8'))
        saved_messages += 1
        sys.stdout.write("saved {} messages\r".format(saved_messages))

    out_file.close()

    print('corpus saved to file {}'.format(out_file_path))

    print('removing temp file')
    os.remove(temp_file_path)

    print('done.')
