mktmpl command
==============

There is a general purpose **mktmpl** command which can be used to generate
your favorite template. It has the following options:

.. code::

    Usage: mktmpl [options]

    Options:
      -h, --help           show this help message and exit
      --debug              debug output
      --tmpl=TMPL          specify template, e.g. EDProducer
      --name=PNAME         specify package name, e.g. MyProducer
      --author=AUTHOR      specify author name
      --ftype=FTYPE        specify file type to generate, e.g. --generate=header,
                           default is all files
      --keep-etags=KETAGS  list examples tags which should be kept in generate
                           code, e.g. --keep-etags='@example_trac,@example_hist'
      --tdir=TDIR          specify template directory,
      --tags               list template tags
      --etags              list template example tags
      --templates          list supported templates

For example if you'd like to generate CMS EDProducer package you can use mktmpl
with the following set of options

.. code::

    mktmpl --tmpl=EDProducer --name=MyProducer

You can list available templates via the following command:

.. code::

    mktmpl --templates

Finally, to list available template and example tags you can use the following
commands:

.. code::

    mktmpl --tmpl=EDProducer --tags
    mktmpl --tmpl=EDProducer --etags
    
