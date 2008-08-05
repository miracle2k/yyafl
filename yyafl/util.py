# Copyright (c) 2008, Yann Ramin
# Copyright (c) 2005, the Lawrence Journal-World
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Django nor the names of its contributors may be used
#        to endorse or promote products derived from this software without
#         specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
