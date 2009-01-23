from distutils.core import setup
setup(
    name = "yyafl",
    version = "0.2.1",
    packages = ['yyafl'],
    author = 'Yann Ramin',
    url = 'http://www.stackfoundry.com/yyafl/',
    download_url = 'http://dl.stackfoundry.org/yyafl/',
    classifiers = [
        'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: User Interfaces',
        ],
    author_email = 'atrus@stackworks.net',
    description = "An easy to use web form generation/domain object, validtion and metadata utility library.",
    long_description = """
Yann's Yet Another Form Library is a web form validtion and metadata library. Forms are created as a special class of domain object, which can then be validated and data extracted, and upon encountering errors, allow the form to be regenerated in HTML for the user's viewing.

YYAFL believes in the separation of style from content, and as such is designed to be used in several different popular templating systems such as Mako and Cheetah, by allowing much of the layout work to be done in the templating system. If you wish to generate more generic, yet still flexible forms, yyafl has support for decorators (Python callables) which are applied when rendering a form as HTML, compatible with basic template callable methods.

"""


)
