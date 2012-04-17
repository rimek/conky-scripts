

class ConkyModule(object):
    obj = None
    name = None
    period = 0

    res_file = None
    tmp_dir = '/tmp/conky-scripts'

    def __init__(self, classname, period):
        self.name = classname.__name__.lower()
        
        self.obj = classname()
        self.period = period


        try:
            os.mkdir(self.tmp_dir)
        except OSError: pass

        self.filename = '%s/%s.result' % (self.tmp_dir, self.name)
        #res_file = open('/tmp/conky/%s.result' % self.name, 'w')

    def try_run(self, counter):
        if not counter % self.period:
            res = self.obj.run()
            self.write_result(res)

    def try_reset(self):
        self.obj.reset()

    def write_result(self, content):
        resfile = open(self.filename, 'w')
        resfile.write(content)
        resfile.close()

    def read_result(self, *argv):
        resfile = open(self.filename, 'r')
        return "".join(resfile.readlines())
            


class ConkyDaemon(Daemon):
    counter = 0
    modules = []

    def __init__(self, *args, **kwargs):
        super(ConkyDaemon, self).__init__(*args, **kwargs)

        setproctitle.setproctitle('conky-scripts')
        self.modules = [ConkyModule(m[0], m[1]) for m in modules]

    def run(self):
        while True:
            for mod in self.modules:
                mod.try_run(self.counter) 

            time.sleep(1)
            self.counter += 1

    def reset_modules(self):
        for mod in self.modules:
            mod.try_reset()

