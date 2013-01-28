Example
=======

Let's create a new template package and call it MyPackage. We will create one
C++ and one header template within this package. We will write associated
module for Skeleton engine and demonstrate how to run your template. Here is
directory structure you should create 

.. code::

    MyPackage/MyPackage.cc
    MyPackage/MyPackage.h

Please note, that template files (MyPackage.cc, MyPackage.h) may have
different names. But if you'd like Skeleton engine to change the name of your
template file according to user settings you need to name your template file
with that name. For example, user wants to create a class Test from your
MyPackage.cc, then Skeleton engine will change MyPackage.cc to Test.cc. While
if you create a template file as TestMyPackageProd.cc the Skeleton engine will
change it to TestTestProd.cc. The **MyPackage** serves as a replacement tag.

Based on Skeleton rules you may use any any word/characters combination
enclosed in double underscored as placeholder tags and package name double
enclosure will be substituted with user settings. For example, let's create a
simple C++ class whose name should be changed. The template will looks like
this:

.. code::

    class __MyPackage__ {
        __MyPackage__(); // constructor
        ~__MyPackage__(); // destructor
    }

if your template name depends on actual MyPackage class you'll write it as
following:

.. code::

    class __MyPackage__: public MyPackage {
        __MyPackage__(); // constructor
        ~__MyPackage__(); // destructor
    }

here the names enclosed with double underscores will be replaced by the package
name of user choice, while base class will not. For example, if user will
choose to create TestPackage (s)he will get the following:

.. code::

    class TestPackage: public MyPackage {
        TestPackage(); // constructor
        virtual ~TestPackage(); // destructor
    }

Here we show examples of MyPackage.cc and MyPackage.h for your convenience.

MyPackage.h example
-------------------

.. code::

    #ifndef __class___ESPRODUCER_h
    #define __class___ESPRODUCER_h
    //
    // class declaration
    //
    class __class__ : public edm::ESProducer {
       public:
          __class__(const edm::ParameterSet&);
          ~__class__();

    #python_begin
        datatypes = []
        for dtype in __datatypes__:
            datatypes.append("boost::shared_ptr<%s>" % dtype)
        return "      typedef edm::ESProducts<%s> ReturnType;" % ','.join(datatypes)
    #python_end

          ReturnType produce(const __record__&);
       private:
          // ----------member data ---------------------------
    };
    #endif // end of __class___ESPRODUCER_h define


    
MyPackage.cc example
--------------------

.. code::

    // -*- C++ -*-
    //
    // Package        :  __name__
    // Class          :  __class__
    // Original Author:  __author__
    //         Created:  __date__

    //
    // constructors and destructor
    //
    __class__::__class__(const edm::ParameterSet& iConfig)
    {
       setWhatProduced(this);
    }

    __class__::~__class__()
    {
       // do anything here that needs to be done at desctruction time
    }


    //
    // member functions
    //

    // ------------ method called to produce the data  ------------
    __class__::ReturnType
    __class__::produce(const __record__& iRecord)
    {
       using namespace edm::es;
    #python_begin
        out1 = []
        out2 = []
        for dtype in __datatypes__:
            out1.append("   boost::shared_ptr<%s> p%s;\n" % (dtype, dtype))
            out2.append("p%s" % dtype)
        output  = '\n'.join(out1)
        output += "   return products(%s);\n" % ','.join(out2)
        return output
    #python_end
    }

    //define this as a plug-in
    DEFINE_FWK_EVENTSETUP_MODULE(__class__);

For these two types of classes we implement the following mypackage.py module

mypackage.py module
-------------------

.. code::

    #!/usr/bin/env python
    #-*- coding: utf-8 -*-
    #pylint: disable-msg=

    """MyPackage module"""

    # package modules
    from Skeletons.pkg import AbstractPkg

    class MyPackage(AbstractPkg):
        "MyPackage implementation of AbstractPkg"
        def __init__(self, config=None):
            if  not config:
                config = {}
            AbstractPkg.__init__(self, config)
            
        def cpp_files(self, kwds):
            "Generate C++ files"
            args = self.config.get('args', None)
            if  not args:
                args = {'__record__': 'MyRecord', '__datatypes__': ['MyData']}
            kwds.update(args)
            return super(ESProducer, self).cpp_files(kwds) 

We re-write `cpp_files` method of AbstractPkg class with our own implementation
details. We define the default tags values to be used in our template and let
user code to pass them via command line arguments. Finally, we create mkmypkg
shell script in Skeletons/bin area with the following context:

.. code::

    #!/bin/sh
    # find out where Skeleton is installed on a system
    sroot=`python -c "import Skeletons; print '/'.join(Skeletons.__file__.split('/')[:-1])"`
    # run actual script
    export SKL_PRGM=mkmypkg
    python $sroot/main.py --type=MyPackage ${1+"$@"} 

With all of thise in place we are ready to use our template as following:

.. code::

    mkmypkg --name=TestPackage "__record__=MyRecord" "__datatypes__=['int',
    'double']"

