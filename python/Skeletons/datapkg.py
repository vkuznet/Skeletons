#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : datapkg.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates DataPkg CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class DataPkg(AbstractPkg):
    "DataPkg implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        dirs = ['doc', 'plugins', 'python', 'test']
        config.update({'dirs':dirs})
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds=None):
        "Generate C++ files"
        kwds.update({'cpp_files':self.get_tmpl('.h') + self.get_tmpl('.xml')})
        kwds.update({'cpp_dir': 'plugins'}) # location of cpp files
        return super(DataPkg, self).cpp_files(kwds)
