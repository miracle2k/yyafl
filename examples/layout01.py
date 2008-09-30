import cherrypy
import yyafl
import yyafl.layout
from yyafl import fields

class Form1(yyafl.Form):
    name = fields.CharField(label = "User name", required = True)
    email = fields.CharField(label = "Your e-mail address", required = True)


class FormTest(object):
    @cherrypy.expose
    def index(self, **kwargs):
        f = Form1(data = kwargs)
        content = ""
        content += """
<html>
<body>
"""
        if f.is_valid() == False:
            content += "Errors: "
            for error in f.errors:
                content += error + " : " + f.errors[error] + "<br />"
        elif f.is_bound and f.is_valid():
            content += "Thanks for the data!"


        content += """
<p>
<form method="GET" action="/">
"""
        l = yyafl.layout.TableLayout(f)
        content += l.render()
        content += "<br /> <input type='submit' value='Submit' /></form>"
        return content


cherrypy.quickstart(root = FormTest())
