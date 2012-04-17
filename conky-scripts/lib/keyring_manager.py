
import keyring
import subprocess

class KeyringManager(object):
    service = None
    name = None

    def __init__(self, name, service):
        self.service = service
        self.name = name

    def get(self, user):
        while(True):
            try:
                password = keyring.get_password(self.service, user)
                if password:
                    return password 
                else:
                    raise "no password in keyring"
            except:
                self.read_and_set(user)

    def set(self, user, password):
        return keyring.set_password(self.service, user, password)

    def read_and_set(self, user):
        title = "%s password" % self.name
        text = 'Enter your password for %(name)s (%(user)s):' % {'name': self.name, 'user': user }

        password = subprocess.check_output([
            'zenity', '--entry', 
            '--title', title,
            '--text',  text,
            '--entry-text', 'password',
            '--hide-text'
            ])
        self.set(user, password.replace("\n", ''))

    def reset(self, user):
        self.set(user, '')
        self.get(user)



