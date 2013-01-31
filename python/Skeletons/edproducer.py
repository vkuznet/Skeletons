#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : edproducer.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates edproducer CMSSW infrastructure
"""
# system modules
import os
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
        if  not kwds.has_key('cpp_dir'):
            kwds.update({'cpp_dir': 'plugins'}) # location for cpp files
        else: # call within SubSystem/Package/plugins area
            kwds.update({'__pkgname__': os.getcwd().split('/')[-2]})
        return super(EDProducer, self).cpp_files(kwds)
