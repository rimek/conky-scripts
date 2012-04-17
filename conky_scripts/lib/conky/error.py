
class ConkyError(Exception):

    def __init__(self, module, filename, error, *args, **kwargs):
        self.filename = filename
        self.error = error
        self.module = module
        super(ConkyError, self).__init__(*args, **kwargs)

    def handle(self):
        self.write_error_to_file()

    def write_error_to_file(self):
        resfile = open(self.filename, 'w')
        resfile.write(unicode(self.error))
        resfile.close()




