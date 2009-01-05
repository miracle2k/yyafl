from distutils.core import setup
setup(
    name = "yyafl",
    version = "0.2.0",
    packages = ['yyafl'],
    author = 'Yann Ramin',
    url = 'http://www.stackfoundry.com/yyafl/',
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
    description = "yyafl is a web form validtion and metadata library",
    long_description = """Yann's Yet Another Form Library is a web form validtion and metadata library.
Forms are created as a special class of domain object, which can then be validated and data extracted.
YYAFL believes in the separation of style from content, and as such is designed to be used
in several different popular templating systems such as Mako and Cheetah.
"""


)
