from subprocess import check_output
import re
import shlex

import os, sys
path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([path, path + '/..'])

from lib.conky.module import ConkyModule

class Pacman(ConkyModule):

    limit = 10 

    command = "sudo pacman -Syup"

    def run(self):
        output = []
        counter = 0

        result = check_output(shlex.split(self.command)) 
        for line in result.split("\n"):
            try:
                match = re.search('(?<=x86_64\/).*(?=.pkg.tar.xz)', line)
                line = match.group(0)
                counter += 1
            except AttributeError: 
                continue

            if counter <= self.limit:
                output.append(line)

        summary = ["Total: %d\n" % counter]
        return  "\n".join(summary + output)


if __name__ == "__main__":

    pacman = Pacman(1)
    print pacman.run()

