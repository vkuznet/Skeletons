#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=
"""
File       : Skeleton.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description:
"""

# system modules
import os
import sys
import pprint
from optparse import OptionParser

if  sys.version_info < (2, 6):
    raise Exception("This script requires python 2.6 or greater")

def tmpl_dir():
    "Retturn default location of template directory"
    return '%s/templates' % '/'.join(__file__.split('/')[:-1])

class SkeletonOptionParser:
    "Skeleton option parser"
    def __init__(self):
        usage  = "Usage: %prog [options]\n"
        self.parser = OptionParser(usage=usage)
        msg  = "debug output"
        self.parser.add_option("--debug", action="store_true",
                default=False, dest="debug", help=msg)
        msg  = "specify template, e.g. EDProducer"
        self.parser.add_option("--tmpl", action="store", type="string",
                default='', dest="tmpl", help=msg)
        msg  = "specify package name, e.g. MyProducer"
        self.parser.add_option("--name", action="store", type="string",
                default="TestPkg", dest="pname", help=msg)
        msg  = "specify author name"
        self.parser.add_option("--author", action="store", type="string",
                default="Creator", dest="author", help=msg)
        msg  = "specify file type to generate, "
        msg += "e.g. --generate=header, default is all files"
        self.parser.add_option("--ftype", action="store", type="string",
                default="all", dest="ftype", help=msg)
        msg  = "list examples tags which should be kept in "
        msg += "generate code, e.g. "
        msg += "--keep-etags='@example_trac,@example_hist'"
        self.parser.add_option("--keep-etags", action="store", type="string",
                default=None, dest="ketags", help=msg)
        msg  = "specify template directory, "
        self.parser.add_option("--tdir", action="store", type="string",
                default=tmpl_dir(), dest="tdir", help=msg)
        msg  = "list template tags"
        self.parser.add_option("--tags", action="store_true",
                default=False, dest="tags", help=msg)
        msg  = "list template example tags"
        self.parser.add_option("--etags", action="store_true",
                default=False, dest="etags", help=msg)
        msg  = "list supported templates"
        self.parser.add_option("--templates", action="store_true",
                default=False, dest="templates", help=msg)
    def get_opt(self):
        "Returns parse list of options"
        return self.parser.parse_args()

def test_env(tdir, tmpl):
    """
    Test user environment, look-up if user has run cmsenv, otherwise
    provide meaningful error message back to the user.
    """
    if  not tdir or not os.path.isdir(tdir):
        print "Unable to acess template dir: %s" % tdir
        sys.exit(1)
    if  not os.listdir(tdir):
        print "No template files found in template dir %s" % tdir
        sys.exit(0)
    if  not tmpl:
        msg  = "No template type is provided, "
        msg += "see available templates via --templates option"
        print msg
        sys.exit(1)

def parse_args(args):
    "Parse input arguments"
    output = {}
    for arg in args:
        key, val = arg.split('=')
        key = key.strip()
        val = val.strip()
        if  val[0] == '[' and val[-1] == ']':
            val = eval(val, { "__builtins__": None }, {})
        output[key] = val
    return output

def generator():
    """
    Code generator function, parse user arguments and load appropriate
    template module. Once loaded, run its data method depending on
    user requested input parameter, e.g. print_etags, print_tags or
    generate template code.
    """
    optmgr = SkeletonOptionParser()
    opts, args = optmgr.get_opt()
    if  opts.debug:
        print obj
        print "Configuration:"
        pprint.pprint(config)
    test_env(os.path.join(opts.tdir, opts.tmpl), opts.tmpl)
    config = {'pname': opts.pname, 'tmpl': opts.tmpl,
              'args': parse_args(args), 'debug': opts.debug,
              'ftype': opts.ftype, 'tmpl_dir': opts.tdir}
    if  opts.ketags:
        etags = opts.ketags.split(',')
        config.update({'tmpl_etags': etags})
    else:
        config.update({'tmpl_etags': []})
    try:
        klass  = opts.tmpl
        mname  = 'Skeletons.%s' % klass.lower()
        module = __import__(mname, fromlist=[opts.tmpl])
        obj    = getattr(module, klass)(config)
    except ImportError as err:
        if  opts.debug:
            print str(err), type(err)
            print "Will use AbstractPkg"
        module = __import__('Skeletons.pkg', fromlist=['AbstractPkg'])
        obj    = getattr(module, 'AbstractPkg')(config)
    if  opts.etags:
        obj.print_etags()
        sys.exit(0)
    elif opts.tags:
        obj.print_tags()
        sys.exit(0)
    elif opts.templates:
        for name in os.listdir(opts.tdir):
            print name
        sys.exit(0)
    obj.generate()

if __name__ == '__main__':
    generator()
