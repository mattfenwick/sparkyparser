from distutils.core import setup

setup(
    name='SparkyParser',
    version='0.0.1',
    packages=['sparkyparser', 
              'sparkyparser.unparse', 
              'sparkyparser.examples',
              'sparkyparser.test'],
    license='MIT',
    author='Matt Fenwick',
    author_email='mfenwick100@gmail.com',
    url='https://github.com/mattfenwick/SparkyParser',
    description='a parser for the NMR Sparky files'
)