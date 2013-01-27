#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : tselector.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates TSelector CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class TSelector(AbstractPkg):
    "TSelector implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds=None):
        "Generate C++ files"
        sources = kwds.get('cpp_files', 
                self.get_tmpl('.cc') + self.get_tmpl('.h') +
                self.get_tmpl('.xml'))
        pkgname = self.config.get('pname')
        kwds.update({'__class__': pkgname, '__name__': pkgname})
        self.gen_files('src', sources, kwds)
