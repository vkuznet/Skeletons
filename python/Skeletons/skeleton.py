#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=

"""
File       : skeleton.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: generates Skeleton CMSSW infrastructure
"""

# system modules
import os
import sys

# package modules
from Skeletons.pkg import AbstractPkg

class Skeleton(AbstractPkg):
    "Skeleton implementation of AbstractPkg"
    def __init__(self, config=None):
        if  not config:
            config = {}
        config.update({'dirs': ['.']})
        AbstractPkg.__init__(self, config)
        
    def dir_structure(self):
        "Generate directory structure"
        if  self.debug:
            print "\nCall dir_structure"

    def cpp_files(self, kwds):
        "Generate C++ files"
        if  self.debug:
            print "\nCall cpp_files"
        args = self.config.get('args', None)
        if  not args:
            args = {'__pkg__': os.getcwd().split('/')[-2]}
        kwds.update(args)
        sources = kwds.get('cpp_files', 
                self.get_tmpl('.cc') + self.get_tmpl('.cpp'))
        pkgname = self.config.get('pname')
        kwds.update({'__class__': pkgname, '__name__': pkgname})
        self.gen_files(os.getcwd(), sources, kwds)

    def header_files(self, kwds):
        "Generate header files"
        if  self.debug:
            print "\nCall header_files"
        args = self.config.get('args', None)
        if  not args:
            args = {'__pkg__': os.getcwd().split('/')[-2]}
        kwds.update(args)
        sources = kwds.get('header_files', 
                self.get_tmpl('.h') + self.get_tmpl('.hpp'))
        pkgname = self.config.get('pname')
        kwds.update({'__class__': pkgname, '__name__': pkgname})
        self.gen_files(os.getcwd(), sources, kwds)
