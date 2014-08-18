
class Element():
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0

    def __repr__(self):
        return "E %(n)s (x,y)=%(x)s,%(y)s"% dict(n=self.id, x=self.x, y=self.y)
