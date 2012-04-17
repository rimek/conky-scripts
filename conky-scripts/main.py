#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

from lib.conky.daemon import ConkyDaemon
from lib.conky.error import ConkyError

from mods.mail import Mail
from mods.ping import Ping
from mods.gitcheck import GitCheck
from mods.pacman import Pacman

modules = ((Mail, 60),
           (Ping, 3),
           (GitCheck, 10),
           (Pacman, 600),
          )

if __name__ == '__main__':

    try:
        daemon = ConkyDaemon('/tmp/conky-scripts.pid', modules=modules)

        if len(sys.argv) == 2:
            if   sys.argv[1] == 'stop': 
                daemon.stop()
                sys.exit(0)
            elif sys.argv[1] == 'restart': 
                daemon.restart()
                sys.exit(0)
            elif sys.argv[1] == 'reset':
                daemon.reset_modules()
                sys.exit(0)

        try:
            daemon.start()
        except: pass

        if len(sys.argv) == 2:
            for module in daemon.modules:
                if sys.argv[1] == module.name:
                    args = sys.argv[2:] if len(sys.argv)>2 else None
                    print module.read_result(args)

    except ConkyError as e:
        e.handle()
        print "* ConkyError raised: ", unicode(e.error)




