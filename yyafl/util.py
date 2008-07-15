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

# Converts a dictionary to a single string with key="value", XML-style with
# a leading space. Assumes keys do not need to be XML-escaped.

def escape(string):
    string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
    return string


flatatt = lambda attrs: u''.join([u' %s="%s"' % (k, escape(v)) for k, v in attrs.items()])


def smart_unicode(s):
    # Create a unicode string if its not a unicode string, using utf-8 encoding
    # Django had this with their settings module
    # Needs to be extended for multiple encodings?
    if not isinstance(s, basestring):
        if hasattr(s, '__unicode__'):
            s = unicode(s)
        else:
            s = unicode(str(s), 'utf-8')
    elif not isinstance(s, unicode):
        s = unicode(s, 'utf-8')
    return s
