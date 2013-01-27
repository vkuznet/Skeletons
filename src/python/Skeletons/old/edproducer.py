#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : edproducer.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates EDProducer CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class EDProducer(AbstractPkg):
    "EDProducer implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        AbstractPkg.__init__(self, config)
        
    def src_files(self, kwds):
        "Generate source files"
        pkgname = self.config.get('pname')
        kwds.update({'__class__': pkgname, '__name__': pkgname})
        return super(EDProducer, self).src_files(kwds)
