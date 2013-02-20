Example
=======

Let's create a new template package and call it MyPackage. This package will
have a header file in include directory and source file in src directory.
We also want to have top-level Makefile. With this set of requirements we
need to create the following template directory

.. code::

    mkdir <path>/scripts/mkTemplates/MyPackage


Here the `<path>` refers to location of Skeleton scripts area. Now we need to
create Driver.dir file which will instruct Skeleton engine about our intention.

.. code::

    cd <path>/scripts/mkTemplates/MyPackage
    cat > Driver.dir << EOF
    Makefile
    src/MyPackage.cc
    include/MyPackage.h
    test
    EOF

Here we created a Driver.dir file with appropriate content. Now let's move on
and create our template files. Our first file is MyPackage.h:

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
        print "      typedef edm::ESProducts<%s> ReturnType;" % ','.join(datatypes)
    #python_end

          ReturnType produce(const __record__&);
       private:
          // ----------member data ---------------------------
    };
    #endif // end of __class___ESPRODUCER_h define

As you may noticed we used Skeleton placeholders tags with double underscores.
(You can use any name surrounded by double underscores and will need to feed
their content via mk-script). Here we use `__class__` to refer the class name
and so on.

Here is content for our MyPackage.cc file:

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
        print output
    #python_end
    }

    //define this as a plug-in
    DEFINE_FWK_EVENTSETUP_MODULE(__class__);

The content of Makefile is not relevant here and can be anything you like.

Finally, we create mkmypkg shell script in Skeletons/bin area with the
following context:

.. code::

    #!/bin/sh
    # find out where Skeleton is installed on a system
    sroot=`python -c "import Skeletons; print '/'.join(Skeletons.__file__.split('/')[:-1])"`
    # run actual script
    export SKL_PRGM=mkmypkg
    python $sroot/main.py --type=MyPackage ${1+"$@"} 

With all of this in place we are ready to use our template as following:

.. code::

    mkmypkg --name=TestPackage "__record__=MyRecord" "__datatypes__=['int',
    'double']"

It will generate the following structure of new package:

.. code::

    TestPackage/
    |  include/
    |  |-- TestPackage.h
    |  src/
    |  |-- TestPackage.cc
    |  test/
    |  Makefile

For more ideas please inspect any of the existing templates, e.g. c++11, which
can be found in Skeleton scripts/mkTemplates/ area.
