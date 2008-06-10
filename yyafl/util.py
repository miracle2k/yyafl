import copy


# SortedDict - maintain insert order of keys
# Used for forms
class SortedDict(dict):

    def __init__(self, data = None):
        if data is None: data = {}
        dict.__init__(self, data)
        self.keyOrder = data.keys()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if key not in self.keyOrder:
            self.keyOrder.append(key)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.keyOrder.remove(key)

    def __iter__(self):
        for k in self.keyOrder:
            yield k

    def items(self):
        return zip(self.keyOrder, self.values())

    def keys(self):
        return self.keyOrder[:]

    def values(self):
        return [dict.__getitem__(self, k) for k in self.keyOrder]

    def update(self, dict):
        for k, v in dict.items():
            self.__setitem__(k, v)

    def setdefault(self, key, default):
        if key not in self.keyOrder:
            self.keyOrder.append(key)
        return dict.setdefault(self, key, default)

    def value_for_index(self, index):
        return self[self.keyOrder[index]]

    def copy(self):
        "Returns a copy of this object."
        obj = self.__class__(self)
        obj.keyOrder = self.keyOrder
        return obj


class SortedDictFromList(SortedDict):
    def __init__(self, data=None):
        if data is None: data = []
        self.keyOrder = [d[0] for d in data]
        dict.__init__(self, dict(data))

    def copy(self):
        return SortedDictFromList([(k, copy.copy(v)) for k, v in self.items()])
