from yyafl.util import flatatt, smart_unicode


class Widget(object):
    is_hidden = False
    def __init__(self, attrs = None):

        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

    def render(self, name, value, attrs = None):
        """ 
        Returns this widget as an HTML entry. 
        """
        raise NotImplementedError
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

class HiddenInput(Input):
    input_type = "hidden"
    is_hidden = True
