
import copy

__all__ = ('Form')


from yyafl.fields import *

# Exceptions
from yyafl.exception import *
from yyafl.util import *

class FieldsMetaclass(type):
    # Inspired heavily by Django
    def __new__(cls, name, bases, attrs):
        fields = [(field_name, attrs.pop(field_name)) for field_name, obj in attrs.items() if isinstance(obj, Field)]
        fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))

        for base in bases[::-1]:
            if hasattr(base, 'base_fields'):
                fields = base.base_fields.items() + fields

        attrs['base_fields'] = SortedDictFromList(fields)
        return type.__new__(cls, name, bases, attrs)



class BaseForm(object):
    def __init__(self, data = None, id = None):
        self.is_bound = data is not None
        self.data = data or {}
        self.clean_data = {}
        self.id = id
        self.errors = {}

        # Has validation been run on this data set
        self.validated = False

        self.fields = self.base_fields.copy()
        if data:
            # Run validation now
            self.validate()

    def bind(self, data, validate = True):
        """ Bind a form with data, optionally running validation.

        If validate == True, will return True for successful validation, or a list of errors.
        If validate == False, will return None.
        """
        self.data = data
        self.is_bound = data is not None
        self.errors = {}
        self.validated = False
        if validate:
            return self.validate()
        else:
            return None


    def __iter__(self):
        for name, field in self.fields.items():
            yield BoundField(self, field, name)

    def __getitem__(self, name):
        try:
            field = self.fields[name]
        except:
            raise KeyError(name)
        return BoundField(self, field, name)


    def get_html_field_name(self, field):
        if self.id is not None:
            return self.id + '_' + field
        else:
            return field

    def is_valid(self):
        if self.errors != {}:
            return False
        if self.data == {}:
            return True
        return True

    def validate(self):
        if self.data == {}:
            return False
        self.errors = {}

        for name, field in self.fields.items():

            try:
                value = self.data[self.get_html_field_name(name)]
                value = field.clean(value)
                self.clean_data[name] = value
            except (ValidationError), e:
                self.errors[name] = e.messages
            except (KeyError), e:
                self.errors[name] = "Value not in request"

        self.validated = True

        if self.errors == {}:
            return True
        else:
            return self.errors



class BoundField(object):
    def __init__(self, form, field, name):
        self.form = form
        self.field = field
        self.name = name

    def __unicode__(self):
        return self.as_widget()

    def as_widget(self, widget = None, **kwargs):
        if not widget:
            widget = self.field.widget
        attrs = kwargs or {}

        for attr in attrs:
            attrs[attr] = unicode(attrs[attr])

        if self.field.id:
            attrs['id'] = self.field.id
        if not self.form.is_bound:
            data = self.field.default
        else:
            data = self.rawvalue
        return widget.render(self.form.get_html_field_name(self.name), data, attrs)


    @property
    def error(self):
        if self.form.validated == False:
            return None
        if self.name in self.form.errors:
            return self.form.errors[self.name]
        else:
            return None

    @property
    def rawvalue(self):
        if self.name in self.form.data:
            return self.form.data[self.name]

    @property
    def value(self):
        if self.name in self.form.clean_data:
            # If its cleaned, get it from the cache
            return self.form.clean_data[self.name]
        else:
            try:
                return self.field.clean(
                    self.form.data[
                        self.form.get_html_field_name(self.name)
                        ]
                    )
            except Exception:
                return None



class Form(BaseForm):
    """ The base form class. Derive from this class to create a form. """
    __metaclass__ = FieldsMetaclass
