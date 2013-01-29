#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : esproducer.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates ESProducer CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class ESProducer(AbstractPkg):
    "ESProducer implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds):
        "Generate C++ files"
        args = self.config.get('args', None)
        if  not args:
            args = {'__record__': 'MyRecord', '__datatypes__': ['MyData']}
        kwds.update(args)
        return super(ESProducer, self).cpp_files(kwds)
