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


from yyafl.util import *

class Layout(object):
    def __init__(self, decorators = None, groups = None):
        self.decorators = decorators
        self.groups = groups

        if self.decorators is None:
            self.decorators = {}

    def decorator_for_field(self, fieldname):
        if fieldname in self.decorators:
            return self.decorators[fieldname]

        if '*' in self.decorators:
            return self.decorators[fieldname]

        return NullDecorator()

    def render(self):
        raise Exception("Not implemented in BaseLayout")


class Decorator(object):
    def __init__(self):
        pass

    def widget_attributes(self, bound_field):
        """ Returns a list of attributes to add or replace in a widget. May not be supported by all widgets. """
        raise Exception("Not implemented")

    def layout_attributes(self, bound_field):
        """ Returns a list of attributes to add to the layout clause for all fo the form field. May not be supported by all layouts. """
        raise Exception("Not implemented")

    def layout_widget_attributes(self, bound_field):
        """ Returns a list of attributes to add to the layout clase for the label for this form field. """
        raise Exception("Not implemented")

    def layout_label_attributes(self, bound_field):
        """ Returns a list of attributes to add to the layout clase for the label for this form field. """
        raise Exception("Not implemented")

    def extra_markup_widget(self, field, rendered_text):
        """ Adds extra markup around a widget. Expects the widget to have already rendered.  """
        raise Exception("Not implemented")

    def extra_markup_label(self, field, rendered_text):
        """ Adds extra markup around a widget. Expects the widget to have already rendered.  """
        raise Exception("Not implemented")


class NullDecorator(Decorator):
    def widget_attributes(self, field):
        return {}

    def layout_attributes(self, field):
        return {}

    def layout_widget_attributes(self, bound_field):
        return {}

    def layout_label_attributes(self, bound_field):
        return {}

    def extra_markup_widget(self, field, rendered_text):
        return rendered_text

    def extra_markup_label(self, field, rendered_text):
        return rendered_text


class NullLayout(Layout):
    def __init__(self,  *args, **kwargs):
        super(NullLayout, self).__init__(*args, **kwargs)

    def render(self, form):
        data = []
        for fieldname in form.fields:
            # Fetch the bound field
            field = form[fieldname]
            field = form[fieldname]

            dec = self.decorator_for_field(field.name)
            data.append(dec.extra_markup_label(field, field.field.label or fieldname))
            widget_attr = dec.widget_attributes(field)
            rendered_widget = field.as_widget(  **widget_attr )
            data.append( dec.extra_markup_widget(field, rendered_widget) )
        return u''.join(data)


class SimpleLayout(Layout):
    """ A SimpleLayout provides basic tags to be worked around a form. Don't use this directly - use a
    TableLayout or DivLayout """

    def __init__(self, *args, **kwargs):
        super(SimpleLayout, self).__init__(*args, **kwargs)
        try:
            self.attributes = kwargs['attributes']
        except:
            self.attributes = {}

    def render_row(self, form, field):
        data = []
        fieldname = field.name
        dec = self.decorator_for_field(fieldname)

        data.append(self.row_begin_tag % flatatt(dec.layout_attributes(field)))
        data.append(self.cell_begin_tag %flatatt(dec.layout_label_attributes(field)))

        data.append(dec.extra_markup_label(field, field.field.label or fieldname))

        data.append(self.cell_end_tag)
        data.append(self.cell_begin_tag % flatatt(dec.layout_widget_attributes(field)))

        widget_attr = dec.widget_attributes(field)

        rendered_widget = field.as_widget(  **widget_attr )

        data.append( dec.extra_markup_widget(field, rendered_widget) )
        data.append(self.cell_end_tag + self.row_end_tag)

        return data

    def render(self, form):
        data = []
        data.append(self.begin_tag % flatatt(self.attributes) )
        for fieldname in form.fields:
            # Fetch the bound field
            field = form[fieldname]
            if field.field.widget.is_hidden:
                # Hidden fields don't need decoration of any details
                data.append(field.as_widget())
                continue
            data.extend( self.render_row(form, field) )

        data.append(self.end_tag)
        return u''.join(data)

class TableLayout(SimpleLayout):
    def __init__(self,  *args, **kwargs):
        super(TableLayout, self).__init__(*args, **kwargs)
        self.begin_tag = u'<table%s>'
        self.end_tag = u'</table>'

        self.row_begin_tag = u'<tr%s>'
        self.row_end_tag = u'</tr>'

        self.cell_begin_tag = u'<td%s>'
        self.cell_end_tag = u'</td>'

class DivLayout(SimpleLayout):
    def __init__(self,  *args, **kwargs):
        super(TableLayout, self).__init__(*args, **kwargs)
        self.begin_tag = u'<div%s>'
        self.end_tag = u'</div>'

        self.row_begin_tag = u'<div%s>'
        self.row_end_tag = u'</div>'

        self.cell_begin_tag = u'<div%s>'
        self.cell_end_tag = u'</div>'
