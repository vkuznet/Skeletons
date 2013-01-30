#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=
"""
File       : cms.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: CMS-related utils
"""

# system modules
import os
import sys

# package modules
from Skeletons.utils import get_code_generator, get_user_info

def config(tmpl, pkg_help, tmpl_dir):
    "Parse input arguments to mk-script"
    kwds  = {'author': '', 'tmpl': tmpl,
             'args': {}, 'debug': False, 'tmpl_dir': tmpl_dir}
    etags = []
    if  len(sys.argv) >= 2: # user give us arguments
        if  sys.argv[1] in ['-h', '--help', '-help']:
            print pkg_help
            sys.exit(0)
        kwds['pname'] = sys.argv[1]
        for idx in xrange(2, len(sys.argv)):
            opt = sys.argv[idx]
            if  opt == '-author':
                kwds['author'] = sys.argv[idx+1]
            if  opt.find('example') != -1:
                etags.append('@%s' % opt)
            if  opt in ['-h', '--help', '-help']:
                print pkg_help
                sys.exit(0)
            if  opt == '-debug':
                kwds['debug'] = True
    elif len(sys.argv) == 1:
        # need to walk
        msg = 'Please enter %s name: ' % tmpl.lower()
        kwds['pname'] = raw_input(msg)
    else:
        print pkg_help
        sys.exit(0)
    kwds['tmpl_etags'] = etags
    return kwds

def cms_error():
    "Standard CMS error message"
    msg  = "\nPackages must be created in a 'subsystem'."
    msg += "\nPlease set your CMSSW environment and go to $CMSSW_BASE/src"
    msg += "\nCreate or choose directory from there and then "
    msg += "\nrun the script from that directory"
    return msg

def test_cms_environment(tmpl):
    """
    Test CMS environment and requirements to run within CMSSW_BASE.
    Return True if we fullfill requirements and False otherwise.
    """
    if  tmpl.lower() == 'skeleton':
        return True
    base = os.environ.get('CMSSW_BASE', None)
    if  not base:
        return False
    cdir = os.getcwd()
    ldir = cdir.replace(os.path.join(base, 'src'), '')
    dirs = ldir.split('/')
    # test if we're within CMSSW_BASE/src/SubSystem area
    if  ldir and ldir[0] == '/' and len(dirs) == 2:
        return 'subsystem'
    # test if we're within CMSSW_BASE/src/SubSystem/src area
    if  ldir and ldir[0] == '/' and len(dirs) == 4 and dirs[-1] == 'src':
        return 'src'
    # test if we're within CMSSW_BASE/src/SubSystem/plugin area
    if  ldir and ldir[0] == '/' and len(dirs) == 4 and dirs[-1] == 'plugin':
        return 'plugin'
    return False

def generate(kwds):
    "Run generator code based on provided set of arguments"
    config = dict(kwds)
    tmpl   = kwds.get('tmpl')
    if  tmpl not in ['Record', 'Skeleton']:
        whereami = test_cms_environment(tmpl)
        if  whereami in ['src', 'plugin']:
            config.update({'ftype': 'cpp'})
        elif whereami == 'subsystem':
            config.update({'ftype': 'all'})
        else:
            print cms_error()
            sys.exit(1)
    obj = get_code_generator(config)
    obj.generate()
