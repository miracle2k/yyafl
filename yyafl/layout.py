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
#     3. Neither the name of StackFoundry nor the names of its contributors may be used
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


class Layout(object):
    def __init__(self, form, decorators = None):
        self.form = form
        self.decorators = decorators
        if self.decoractors is None:
            self.decorators = {}

    def decorator_for_field(self, fieldname):
        # TODO: Extend this for wildcards
        try:
            return decorators[fieldname]
        except:
            return NullDecorator()

    def layout(self):
        raise Exception("Not implemented in BaseLayout")


class Decorator(object):
    def __init__(self):
        pass

    def widget_attributes(self, bound_field):
        """ Returns a list of attributes to add or replace in a widget. May not be supported by all widgets. """
        raise Exception("Not implemented")

    def layout_attributes(self, bound_field):
        """ Returns a list of attributes to add to the layout clause for this form field. May not be supported by all layouts. """
        raise Exception("Not implemented")

    def extra_markup(self, field, rendered_text):
        """ Adds extra markup around a widget. Expects the widget to have already rendered.  """
        raise Exception("Not implemented")

class NullDecorator(Decorator):
    def widget_attributes(self, field):
        return []

    def layout_attributes(self, field):
        return []

    def extra_markup(self, field, rendered_text):
        return rendered_text


class NullLayout(Layout):
    def __init__(self, form, *args, **kwargs):
        super(NullLayout, self).__init__(form, *args, **kwargs)
    def layout(self):
        data = []
        for field in self.form.fields:
            # Fetch the bound field
            field = self.form[field.name]

            dec = self.decorator_for_field(field.name)
            widget_attr = {}
            if dec:
                widget_attr = dec.widget_attributes(field)
            data.append(field.as_widget(  **widget_attr ))

        return u''.join(data)


class TableLayout(Layout):
    def __init__(self, form,  *args, **kwargs):
        super(TableLayout, self).__init__(form, *args, **kwargs)
    def layout(self):
        data = []
        data.append(u'<table>')
        for field in self.form.fields:
            # Fetch the bound field
            field = self.form[field.name]

            data.append(u'<tr%s><td>' % flatatt(self.decorator_for_field(field.name).layout_attributes(field)))
            data.append(field.field.label)
            data.append(u'</td><td>')
            dec = self.decorator_for_field(field.name)

            widget_attr = dec.widget_attributes(field)

            rendered_widget = field.as_widget(  **widget_attr )

            data.append( dec.extra_markup(field, rendered_widget) )
            data.append(u'</td></tr>')

        return u''.join(data)
