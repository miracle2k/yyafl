from setuptools import setup, find_packages
setup(
    name = "yyafl",
    version = "0.2.1",
    packages = find_packages(),
    author = 'Yann Ramin',
    author_email = 'atrus@stackworks.net',
    description = "Yann's Yet Another Form Library is a web form validtion and metadata library",
    long_description = """Yann's Yet Another Form Library is a web form validtion and metadata library.
Forms are created as a special class of domain object, which can then be validated and data extracted.
YYAFL believes in the separation of style from content, and as such is designed to be used
in several different popular templating systems such as Mako and Cheetah.
"""


)
