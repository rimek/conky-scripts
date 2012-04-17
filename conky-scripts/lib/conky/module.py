import os

from lib.conky.error import ConkyError

class ConkyModule(object):

    class Meta:
        abstract = True

    name = None
    period = 0

    res_file = None
    tmp_dir = '/tmp/conky-scripts'

    def __init__(self, period):
        self.name = self.__class__.__name__.lower()
        self.period = period
        try:
            os.mkdir(self.tmp_dir)
        except OSError: pass
        self.filename = '%s/%s.result' % (self.tmp_dir, self.name)

    def prepare(self): pass
    def run(self):     pass
    def reset(self):   pass

    def try_run(self, counter):
        if not counter % self.period:
            res = self.run()
            self.write_result(res)

    def try_reset(self):
        try: 
            self.reset()
        except AttributeError as e:
            raise ConkyError(self, self.filename, e)

    def write_result(self, content):
        resfile = open(self.filename, 'w')
        resfile.write(content)
        resfile.close()

    def read_result(self, *argv):
        resfile = open(self.filename, 'r')
        return "".join(resfile.readlines())
            


