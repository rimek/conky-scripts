
from subprocess import check_output
import shlex
import re

import os, sys
path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([path, path + '/..'])

from lib.conky.module import ConkyModule

class Ping(ConkyModule):

    hosts = (('google', 'google.pl'), 
             ('home', 'm.rimek.org'), 
             ('router', 'router'),
             ('storage', 'storage'))

    command = "ping -n -c 1 -W 1 %s" #  | grep '64 bytes from ' | sed -e 's/.*time=//; s/ ms.*//' 2>/dev/null"


    def run(self):
        output = [] 

        for (name,host) in self.hosts:
            raw = check_output(shlex.split(self.command % host)) 

            res = ''
            for line in raw.split("\n"):
                if '64 bytes from' in line:
                    res = line

            res = re.search('(?<=time\=).*(?=\ ms)', res).group(0) if res else ''
            output.append("%s $alignr ${color orange}%s$color" % (host, res))

        return "\n".join(output)

    def prepare(self): pass
    def reset(self): pass


if __name__ == "__main__":
    ping = Ping(1)
    print ping.run()

