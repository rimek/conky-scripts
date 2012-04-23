from subprocess import call 

import os, sys
path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([path, path + '/..'])

from lib.conky.module import ConkyModule

class GitCheck(ConkyModule):

    repos = (('configs', '~/configs/files'), 
             ('serials', '/add/projekty/linux/serialwatcher'), 
             ('timesheet', '/kp'))

    command = """ cd %s;
        git update-index --refresh;
        git diff-index --quiet HEAD --;
    """

    def run(self):
        output = []
        for (name,repo) in self.repos:
            repo = os.path.expanduser(repo)
            if not os.path.exists(repo):
                res = "${color orange}not exist$color"
            else:
                retcode = call(self.command % repo, shell=True) 
                res = "${color red}changed$color" if retcode else "ok"
            output.append("%s $alignr %s" % (name, res))
        return "\n".join(output)


if __name__ == "__main__":
    git = GitCheck(1)
    print git.run()

