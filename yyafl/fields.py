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

from yyafl.exception import ValidationError

import re
import gettext
_trans = gettext.translation('yyafl', fallback = True)
_ = _trans.ugettext

from widgets import TextInput, Select
from yyafl.util import smart_unicode

EMPTY_VALUES = ["", u"", None, " "]


class Field(object):

    creation_counter = 0

    def __init__(self, required = True, label = None, id = None, default = None, widget = None):
        self.required = required
        self.default = default
        self.label = label
        self.id = id
        self.widget = widget or TextInput
        self.widget = self.widget()
        # Up the creation counter
        # Idea borrowed from Django to sort fields
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def clean(self, value):
        if self.required and value in EMPTY_VALUES:
            raise ValidationError(_(u'Value is required.'))
        return value



class CharField(Field):
    def __init__(self, max_length = 100, min_length = 0, *args, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        super(CharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CharField, self).clean(value)
        value = smart_unicode(value)

        if value in EMPTY_VALUES:
            return u''

        if len(value) > self.max_length:
            raise ValidationError(_(u'Value can only be up to %d characters long') % self.max_length)
        if len(value) < self.min_length:
            raise ValidationError(_(u'Value must be at least %d characters long') % self.min_length)

        return value


# Inspired by Django

class RegexField(Field):
    def __init__(self, regex, max_length = None, min_length = None, error_message = None, *args, **kwargs):
        super(RegexField, self).__init__(*args, **kwargs)
        if isinstance(regex, basestring):
            regex = re.compile(regex)
        self.regex = regex
        self.max_length, self.min_length = max_length, min_length
        self.error_message = error_message or _(u'Enter a valid value.')

    def clean(self, value):
        super(RegexField, self).clean(value)
        if value in EMPTY_VALUES:
            value = u''
        value = smart_unicode(value)
        if value == u'':
            return value
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(_(u'Value must have has at most %d characters.') % self.max_length)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(_(u'Value must have at least %d characters.') % self.min_length)
        if not self.regex.search(value):
            raise ValidationError(self.error_message)
        return value

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

class EmailField(RegexField):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        RegexField.__init__(self, email_re, max_length, min_length,
            _(u'Enter a valid e-mail address.'), *args, **kwargs)



class IntegerField(Field):
    def __init__(self, min_value = None, max_value = None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super(IntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if value in EMPTY_VALUES:
            return None
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(_(u'Enter an integer value (i.e.: -1, 10, 3000)'))
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(_(u'Value must be less than %d') % self.max_value)
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(_(u'Value must be greater than %d') % self.min_value)
        return value


class FloatField(Field):
    def __init__(self, min_value = None, max_value = None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super(IntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if value in EMPTY_VALUES:
            return None
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(_(u'Enter a number'))
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(_(u'Value must be less than %d') % self.max_value)
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(_(u'Value must be greater than %d') % self.min_value)
        return value


class ChoiceField(Field):
    def __init__(self, allowed_values = [], widget = None, *args, **kwargs):
        self.allowed_values = allowed_values
        super(ChoiceField, self).__init__(*args, **kwargs)
        self.widget = widget or Select
        self.widget = self.widget()

    def clean(self, value):
        if value in self.allowed_values:
            return value
        else:
            raise ValidationError(_(u'Not an allowed value.'))
