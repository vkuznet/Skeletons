#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : evhypothesis.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates EventHypothesis CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class EventHypothesis(AbstractPkg):
    "EventHypothesis implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        dirs = ['doc', 'plugins', 'python', 'test']
        config.update({'dirs':dirs})
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds=None):
        "Generate C++ files"
        sources = kwds.get('cpp_files', 
                self.get_tmpl('.cc') + self.get_tmpl('.h'))
        pkgname = self.config.get('pname')
        kwds.update({'__class__': pkgname, '__name__': pkgname})
        self.gen_files('plugins', sources, kwds)
