
from yyafl import ValidationError

import gettext
_trans = gettext.translation('yyafl', fallback = True)
_ = _trans.ugettext

EMPTY_VALUES = ["", u"", None, " "]

def smart_unicode(s):
    # Create a unicode string if its not a unicode string
    if not isinstance(s, basestring):
        if hasattr(s, '__unicode__'):
            s = unicode(s)
        else:
            s = unicode(str(s), 'utf-8')
    elif not isinstance(s, unicode):
        s = unicode(s, 'utf-8')
    return s


class Field:
    def __init__(self, required = True, label = None, default = None):
        self.required = required
        self.default = default

    def clean(self, value):
        if self.required and value in EMPTY_VALUES:
            raise ValidationError(_(u'Value is required.')))
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
    def __init__(self, regex, max_length=None, min_length=None, error_message=None, *args, **kwargs):
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



def IntegerField(Field):
    def __init__(self, min_value = None, max_value = None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super(IntegerField, self).__init__(*args, **kwargs)
    def clean(value):
        if value in EMPTY_VALUES:
            return None
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(_(u'Enter an integer value (-1, 10, 3)'))
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(_(u'Value must be less than %d') % self.max_value)
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(_(u'Value must be greater than %d') % self.min_value)
        return value




