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
        skl = os.environ.get('SKL_PRGM', None)
        if  skl:
            usage  = "Usage: %s [options]\n" % skl
        else:
            usage  = "Usage: %prog [options]\n"
        usage += "More help should go here ...."
        self.parser = OptionParser(usage=usage)
        msg  = "debug output"
        self.parser.add_option("--debug", action="store_true",
                default=False, dest="debug", help=msg)
        msg  = "specify package type, e.g. EDProducer"
        self.parser.add_option("--type", action="store", type="string", 
                default='EDProducer', dest="ptype", help=msg)
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

def test_env():
    """
    Test user environment, look-up if user has run cmsenv, otherwise
    provide meaningful error message back to the user.
    """
    cmssw = os.environ.get('CMSSW_BASE', '')
    sdir  = os.path.join(cmssw, 'src')
    if  not cmssw or not os.path.isdir(sdir) or \
        os.getcwd() != sdir:
        msg  = "Packages must be created in a 'subsystem'."
        msg += "\nPlease set your CMSSW environment and go to $CMSSW_BASE/src"
        msg += "\nCreate or choose directory from there and then "
        msg += "run the script from that directory"
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
    test_env()
    config = {'pname': opts.pname, 'ptype': opts.ptype,
              'args': parse_args(args), 'debug': opts.debug,
              'ftype': opts.ftype, 'tdir': opts.tdir}
    if  opts.ketags:
        etags = opts.ketags.split(',')
        config.update({'tmpl_etags': etags})
    else:
        config.update({'tmpl_etags': []})
    if  opts.templates:
        for name in os.listdir(opts.tdir):
            print name
        sys.exit(0)
    try:
        klass  = opts.ptype
        mname  = 'Skeletons.%s' % klass.lower()
        module = __import__(mname, fromlist=[opts.ptype])
        obj    = getattr(module, klass)(config)
    except Exception as err:
        if  opts.debug:
            print str(err)
            print "Will use AbstractPkg"
        module = __import__('Skeletons.pkg', fromlist=['AbstractPkg'])
        obj    = getattr(module, 'AbstractPkg')(config)
    if  opts.debug:
        print obj
        print "Configuration:"
        pprint.pprint(config)
    if  opts.etags:
        obj.print_etags()
    elif opts.tags:
        obj.print_tags()
    else:
        obj.generate()

if __name__ == '__main__':
    generator()
