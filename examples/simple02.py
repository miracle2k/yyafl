import cherrypy
import yyafl
from yyafl import fields

class Form1(yyafl.Form):
    name = fields.CharField()
    email = fields.CharField()


class FormTest(object):

    @cherrypy.expose
    def index(self, **kwargs):
        f = Form1(data = kwargs)
        content = ""
        content += """<html><body>"""

        if f.is_valid() == False:
            content += "Errors: "
            for error in f.errors:
                content += error + " : " + f.errors[error] + "<br />"
        elif f.is_bound and f.is_valid():
            content += "Thanks for the data!"


        content += """<p><form method="GET" action="/">Please enter your name and e-mail:<br/>Name: """
        content += f['name'].as_widget()

        if f['name'].error:
            content += f['name'].error
        content += """<br />E-mail: """
        content += f['email'].as_widget(attrs = {'size' : '100'})

        if f['email'].error:
            content += f['email'].error
        content += """<br /><input type="submit" /></body></html>"""

        return content

if __name__ == '__main__':
    cherrypy.quickstart(root = FormTest())
