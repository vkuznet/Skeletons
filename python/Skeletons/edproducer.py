#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : edproducer.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates edproducer CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class EDProducer(AbstractPkg):
    "EDProducer implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        dirs = ['doc', 'plugins', 'python', 'test']
        config.update({'dirs':dirs})
        AbstractPkg.__init__(self, config)
        
    def cpp_files(self, kwds):
        "Generate C++ files"
        kwds.update({'cpp_dir': 'plugins'}) # location for cpp files
        return super(EDProducer, self).cpp_files(kwds)
