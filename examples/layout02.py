import cherrypy
import yyafl
import yyafl.layout
from yyafl import fields
from yyafl.widgets import HiddenInput

# This example covers the user of custom decorators for required form fields

class Form1(yyafl.Form):
    name = fields.CharField(label = "User name", required = True)
    email = fields.CharField(label = "Your e-mail address", required = True)
    optional = fields.CharField(label = "Optional field", required = False)
    hidden = fields.CharField(widget = HiddenInput, default = "123")
    _layout = yyafl.layout.TableLayout()

class RequiredDecorator(yyafl.layout.NullDecorator):
    def extra_markup_widget(self, field, rendered_text):
        if field.required:
            return rendered_text + " * "
        return rendered_text

class FormTest(object):

    @cherrypy.expose
    def index(self, **kwargs):
        f = Form1(data = kwargs)
        # Add a global decorator
        f.layout().add_decorator('*', RequiredDecorator())
        content = ""
        content += "<html><body>"

        if f.is_valid() == False:
            content += "Errors: "
            for error in f.errors:
                content += error + " : " + f.errors[error] + "<br />"
        elif f.is_bound() and f.is_valid():
            content += "Thanks for the data!"


        content += "<p><form method=\"GET\" action=\"/\">"

        # Render using the layout specified in _layout above.
        content += f.render()
        # Or invoke the layout explicitly
        # l = yyafl.layout.TableLayout()
        # l.render(f)

        content += "<br /> <input type='submit' value='Submit' /></form>"
        return content


if __name__ == '__main__':
    cherrypy.quickstart(root = FormTest())
