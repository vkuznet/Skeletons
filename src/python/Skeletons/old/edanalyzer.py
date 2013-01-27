#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=
"""
File       : edanalyzer.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates EDAnalyzer CMSSW infrastructure
"""

# package modules
from Skeletons.pkg import AbstractPkg

class EDAnalyzer(AbstractPkg):
    "EDAnalyzer implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        AbstractPkg.__init__(self, config)
        
    def src_files(self, kwds):
        "Generate source files"
        kwds.update({'__class__': self.config.get('name')})
        return super(EDAnalyzer, self).src_files(kwds)
