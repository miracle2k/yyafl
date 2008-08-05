# Copyright (c) 2008, Yann Ramin
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

import yyafl.fields

from yyafl.util import flatatt, smart_unicode
from yyafl.exception import IncompatibleWidget




class Widget(object):
    is_hidden = False
    def __init__(self, attrs = None):

        self.field = None

        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

    def render(self, name, value, attrs = None):
        """
        Returns this widget as an HTML entry.
        """
        raise NotImplementedError
    def set_field(self, field):
        """ Capture or return the Field instance """
        if field:
            self.field = field
        return self.field
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs


class Input(Widget):
    input_type = None # Subclasses must define this.

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '': final_attrs['value'] = smart_unicode(value)
        return u'<input%s />' % flatatt(final_attrs)

class TextInput(Input):
    input_type = "text"
    pass

class TextArea(Widget):
    def render(self, name, value, attrs = None):
        if value is None: value = '' # default value
        final_attrs = self.build_attrs(attrs, name=name)

        return u'<textarea' + flatatt(final_attrs) + u'>' + smart_unicode(value) + u'</textarea>'

class Select(Widget):

    def _get_value(self, value):
        # Fetch the value from the list or dict
        values = self.field.allowed_values
        if isinstance(values, list):
            return smart_unicode(value)
        else:
            return smart_unicode(values[value])

    def render(self, name, value, attrs = None):
        if value is None: value = '' # default value
        final_attrs = self.build_attrs(attrs, name=name)
        options = []
        if not isinstance(self.field, yyafl.fields.ChoiceField):
            raise IncompatibleWidget(u'Widget named %s is incompatible with select' % name)

        for option in self.field.allowed_values:
            option_attrs = {'value' : option }
            if value == option:
                option_attrs['selected'] = u'selected'

            options.append(u'<option %s>' % flatatt(option_attrs) +  self._get_value(option) + u'</option>')

        return u'<select' + flatatt(final_attrs) + u'>' + u''.join(options) + u'</select>'


class HiddenInput(Input):
    input_type = "hidden"
    is_hidden = True
