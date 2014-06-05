## SparkyParser ##

A library for parsing data in the Sparky format, used
by the Sparky analysis program NMR (Nuclear Magnetic Resonance).

This is an open source project under the MIT license; 
feel free to use the code in any way that helps you get
some awesome science done!



## Project file grammar ##

    End         :=  not0(/./)

    Newline     :=  '\n'
    
    Tag(p)      :=  '<'  p  '>'  ( Newline  |  End )

    String      :=  /[^<>\s]+/

    Line        :=  String(+)  Newline

    Datum       :=  Line  |  Block

    Block       :=  Tag(name)  Datum(*)  Tag('end', name)
    
    Version     :=  Tag('version', String)

    Type        :=  Tag('sparky', String, 'file')

    Proj        :=  Type  Version  Block(*)  End

Ignored white space: spaces and tabs

## Save file grammar ##



### Installation ###

The easiest way to install SparkyParser is using pip:

    $ pip install sparkyparser

If you don't have pip or easy_install, you can download the package
manually from [the pypi page](https://pypi.python.org/pypi/SparkyParser).


### Quick Start ###




### Python version ###

This library was created for use with Python2.7.  Although it may work
with other Python versions, I haven't tried that.

 

### Contact information ###

Found a bug?  Need help figuring something out?  Want a new feature?  Feel free
to report anything using the github issue tracker, or email me directly at
mfenwick100 at gmail dot com
