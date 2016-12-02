import json

class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = json.loads(open(self.filename, 'r').read())


    def save(self):
        with open(self.filename, 'w') as outf:
            outf.write(
                json.dumps(
                    self.config,
                    indent=4,
                    sort_keys=True)
            )


    def reload(self):
        self.config = json.loads(open(self.filename, 'r').read())


    def add(self, param):
        self.config[param[0]] = param[1]
        self.save()


    def remove(self, paramname):
        if self.config.get(paramname) is not None:
            del self.config[paramname]
        self.save()
