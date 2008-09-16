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

    def layout(self):
        raise Exception("Not implemented in BaseLayout")


class Decorator(object):
    def __init__(self):
        pass

    def widget_attributes(self):
        """ Returns a list of attributes to add or replace in a widget. May not be supported by all widgets. """
        raise Exception("Not implemented")

    def layout_attributes(self):
        """ Returns a list of attributes to add to the layout clause for this form field. May not be supported by all layouts. """
        raise Exception("Not implemented")

    def extra_markup(self, widget):
        """ Adds extra markup around a widget. """
        raise Exception("Not implemented")

class NullDecorator(Decorator):
    def widget_attributes(self):
        return []

    def layout_attributes(self):
        return []

    def extra_markup(self, widget):
        return widget


class NullLayout(Layout):
    def __init__(self, form, *args, **kwargs):
        super(NullLayout, self).__init__(form, *args, **kwargs)


class TableLayout(Layout):
    def __init__(self, form,  *args, **kwargs):
        super(TableLayout, self).__init__(form, *args, **kwargs)
        self._decorators = decorators
