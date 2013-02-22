#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import imaplib
from email.header import decode_header

import os, sys
path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([path, path + '/..'])

from lib.conky.module import ConkyModule
from lib.keyring_manager import KeyringManager

class Mail(ConkyModule):

    boxes = (('Inbox', 'Inbox'), 
             ('Allegro', 'Allegro'),
             ('Home', 'Home'),
             ('Aktualnosci', 'Aktualnosci'),
             ('UPC', 'UPC'))

    def prepare(self, user = 'rimeczek'):
        self.user = user
        self.key_manager = KeyringManager('Conky Mail Checker', 'conky-services-mail')
        self.passwd = self.key_manager.get(user)
        self.host = 'imap.gmail.com'

    def check_imap_folder(self, foldername):
        list = []
        imap = imaplib.IMAP4_SSL(self.host)
        imap.login(self.user, self.passwd)
        imap.select(foldername, 1)
        typ, data = imap.search(None, 'UNSEEN')

        for msg in data[0].split():
            typ, data = imap.fetch(msg, '(RFC822.SIZE BODY[HEADER.FIELDS (FROM)])')
            list.append(decode_header(data[0][1].lstrip('From: ').strip() + ' ')[0][0])

        imap.logout()
        return list 

    def check(self):
        result = ""
        mail_count = 0
        boxlist = {}

        format_normal = "%s. %s\n"
        format_color  = "${color1}%s. %s${color}\n"

        for (name,box) in self.boxes: 
            boxlist[name] = self.check_imap_folder(box)

        for boxname in boxlist:
            box = boxlist[boxname]
            mail_count += len(box)

            if len(box) == 0: continue

            result += "${color2}%s$color\n" % boxname

            i = 0
            for msg in box:
                i += 1
                msg_tuple = (i, msg[:30])

                result += format_normal % msg_tuple if i>2 else \
                          format_color  % msg_tuple

        if mail_count == 0:
            result = "Brak nowej poczty"
        return result

    def run(self):
        return self.check()

    def reset(self):
        self.key_manager.reset(self.user)

def NeublocMail(Mail):
    boxes = (('Inbox', 'Inbox'),)

    def __init__(self, period):
        Mail.__init__(self,period)

    def prepare(self, user = 'mrim@neubloc.net'):
        self.user = user
        self.key_manager = KeyringManager('Conky Mail Checker',
                'conky-services-mail-neubloc')
        self.passwd = self.key_manager.get(user)
        self.host = 'imap.secureserver.net'



if __name__ == '__main__':
    m = NeublocMail(1)
    m.prepare()

    if len(sys.argv) == 2:
        if sys.argv[1] == 'reset':
            m.reset()

    print m.run()






