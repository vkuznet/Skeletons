Package Templates
=================

Skeletons template system uses user-defined templates which may have arbitrary
file structure within template directory. The name of template directory defines a
template type available to the end-users.

In order to extend Skeletons package with your own template package you need
to create it within scripts/mkTemplates area of Skeletons package. The new
template package may contain arbitrary set of files and any directory
structure. But you need to provide a `Driver.dir` file with such structure.
For instance, if you want to create template package `Foo` with
src/test/include directories, Foo.cc file in src area, Foo.h in include area
and top-level makefile your `Driver.dir` file will have the following structure:

.. code::

    Makefile
    src/Foo.cc
    test/
    include/Foo.h

In order to write your template files, e.g. Foo.cc, Foo.h and Makefile, please
consult Skeletons rules section.

Skeletons rules
---------------

There are two types of tags supported by Skeletons package, template and example
tags. Template tags can use any name which should be enclosed with double
underscores, e.g. `__test__`, `__prodname__`, `__abc123__`. The example tags
should start with `@example_` prefix followed by the name, e.g. `@example_track`.

In addition to template and example tags, user can write python snippets in their
template, which should be enclosed with two statements: `#python_begin` and 
`#python_end`. PLEASE NOTE: you must use proper identination for python snippets
similar to normal python code requirements.

For example:

.. code::

    #python_begin
        output = []
        for dtype in __datatypes__:
            ptr = "std::shared_ptr<%s> p%s;" % dtype
            output.append(ptr)
        print output
    #python_end

Here we created an output vector which stores strings of shared pointers for
data types found in __datatypes__ template tag. Finally we printed out output
vector content. Any print statement will be captured and its context will be
added to your templates.  In this case if you supply __datatypes__ with array
of data types you want to create in python snippet, e.g. __datatypes__=['int',
'double'], the Skeletons engine will replace this python snippet with the
following:

.. code::

    std::shared_ptr<int> pint;
    std::shared_ptr<double> pdouble;


Event though we do not impose any restriction on tag naming convention it is
wise to use them appropriately, e.g. for your C++ class template you are better
use `__class__` and similar tag name conventions.

Driver.dir file
---------------

In some cases you'd like to generate your template according to some directory
structure. To make this happens you need to place into your template package
the `Driver.dir` file whose context should outline a final directory structure
of generated package. For instance, let's say that your template package has
source and header c++ files as well as Makefile:

.. code::

    MyPackage.cc, MyPackage.h, Makefile

and you'd like to create the following directory layout:

.. code::

    MyPackage
    |-- Makefile
    |   include/
    |   |-- MyPackage.h
    |   src/
    |   |-- MyPackage.cc

To instruct Skeletons engine to generate such directory structure and put files
in place you create `Driver.dir` inside of your package template with the
following context:

.. code::

    Makefile
    incldue/MyPackage.h
    src/MyPackage.cc

The Skeletons engine will use theis file, create include,
src directories and place generated files in appropriate locations.
