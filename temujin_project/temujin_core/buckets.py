
class Bucket(object):
    pass



class FileBucket(object):
    def __init__(self, base_path):
        self.base_path = base_path


    def get_path(self, ns, name):
        return os.path.join(self.base_path, ns, name)
    

    def get_ns(self, ns):
        path = os.path.join(self.base_path, ns)
        try:
            os.mkdir(path)
        except:
            pass


    def get(ns, key):
        filename = self.get_path(ns, key)
        with open(filename) as f:
            return f.read()

    def set(ns, key, data):
        filename = self.get_path(ns, key)
        with open(filename, "wb") as f:
            f.write(data)

    def delete_ns(self, name):
        path = os.path.join(self.base_path, ns)
        os.rmdir(path)

    



