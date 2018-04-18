class Node:
    def __init__(self, data, parent=None, child=[], mark=False):
        self.data = data
        self.parent = parent
        self.child = child
        self.mark = mark

    def getData(self):
        return self.data

    def getChild(self, i):
        return self.child[i]

    def setData(self, data):
        self.data = data

    def setChild(self, list_child):
        self.child = list_child

    def addChild(self, item):
        self.child.append(item)

    def getNumChild(self):
        return len(self.child)
