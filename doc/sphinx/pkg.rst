Package Templates
=================

Skeletons template system uses user-defined templates which may have arbitrary
files within template directory. The name of template directory defines a
template type available to the end-users.

In order to extend Skeletons package with your own package template(s) you need
to fullfill the following requirements:

    - create a new package in Skeletons/src/python/Skeletons/templates area,
      e.g. MyPackage
    - place any type template inside your package, e.g.
      MyPackage/MyPackage.cc
    - write your template according to Skeletons rules (see below)
    - optionally create a new python module in Skeletons/src/python/mypackage.py
      with class inherited from AbstractPkg with your implementation of rules,
      e.g. `class MyPackage(AbstractPkg)`, see below for comlpete examples

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

Implementation rules
--------------------

To implement your own template class you need to create a new python module
(possibly with the same name as your template package) and inherit its code
from AbstractPkg class. We advocate to follow standard python conventions, i.e.
module name should be lower case, e.g. mypackage.py, you match your python
module name with your template package, e.g. mypackage.py should cover
MyPackage template. Finally you implement some of the main template methods of
the AbstractPkg class. They are cpp_files, python_files, test_files, etc.
Please follow Skeletons rules to create your template and use reasonable
template and example tags inside of your template. For example, when you write
a C++ class it is appropriate to use template tags as `__class__`,
`__header__`, while for any other type of template you may use their own
language specific tags.
