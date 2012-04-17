
import time
import setproctitle

from lib.daemon import Daemon
from lib.conky.error import ConkyError

class ConkyDaemon(Daemon):
    counter = 0
    modules = []

    def __init__(self, *args, **kwargs):
        setproctitle.setproctitle('conky-scripts')
        modules = kwargs['modules']
        del kwargs['modules']

        kwargs['stdout'] = '/tmp/conky-scripts.out'
        kwargs['stderr'] = '/tmp/conky-scripts.out'
        super(ConkyDaemon, self).__init__(*args, **kwargs)

        self.modules = [modclass(modperiod) for (modclass, modperiod) in modules]

    def run(self):
        [mod.prepare() for mod in self.modules]

        while True:
            for mod in self.modules:
                try:
                    mod.try_run(self.counter) 
                except Exception as e:
                    ConkyError(mod, mod.filename, e).handle()
            time.sleep(1)
            self.counter += 1

    def reset_modules(self):
        for mod in self.modules:
            try:
                mod.prepare()
                mod.try_reset()
            except Exception as e:
                ConkyError(mod.obj, mod.filename, e).handle()

