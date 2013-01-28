#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable-msg=W0122,R0914,R0912

"""
File       : pkg.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: AbstractGenerator class provides basic functionality
to generate CMSSW class from given template
"""

# system modules
import os
import sys
import time
import pprint

# package modules
from Skeletons.utils import parse_word, functor, get_user_info

class AbstractPkg(object):
    """
    AbstractPkg takes care how to generate code from template/PKG
    package area. The PKG can be any directory which may include
    any types of files, e.g. C++ (.cc), python (.py), etc.
    This class relies on specific logic which we outline here:

        - each template may use tags defined with double underscores
          enclosure, e.g. __class__, __record__, etc.
        - each template may have example tags, such tags should
          start with @example_. While processing template user may
          choose to strip them off or keep the code behind those tags
        - in addition user may specify pure python code which can
          operate with user defined tags. This code snipped should
          be enclosed with #python_begin and #python_end lines
          which declares start and end of python block
    """
    def __init__(self, config=None):
        super(AbstractPkg, self).__init__()
        if  not config:
            self.config = {}
        else:
            self.config = config
        dirs = ['doc', 'interface', 'python', 'src', 'test']
        if  not self.config.has_key('dirs'):
            self.config.update({'dirs': dirs})
        self.pname = self.config.get('pname', None)
        self.tmpl  = self.config.get('tmpl', None)
        self.debug = self.config.get('debug', 0)
        self.tdir  = self.config.get('tmpl_dir')
        author, office = get_user_info()
        if  office:
            self.author = '%s, %s' % (author, office)
        else:
            self.author = author
        self.date  = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        self.rcsid = '$Id$'
        
    def tmpl_etags(self):
        "Scan template files and return example tags"
        keys = []
        sdir = '%s/%s' % (self.tdir, self.tmpl)
        for name in os.listdir(sdir):
            if  name[-1] == '~':
                continue
            fname = os.path.join(sdir, name)
            with open(fname, 'r') as stream:
                for line in stream.readlines():
                    if  line.find('@example_') != -1: # possible tag
                        keys += [k for k in line.split() if \
                                    k.find('@example_') != -1]
        return set(keys)

    def print_etags(self):
        "Print out template example tags"
        for key in self.tmpl_etags():
            print key

    def tmpl_tags(self):
        "Scan template files and return template tags"
        keys = []
        sdir = '%s/%s' % (self.tdir, self.tmpl)
        for name in os.listdir(sdir):
            if  name[-1] == '~':
                continue
            fname = os.path.join(sdir, name)
            with open(fname, 'r') as stream:
                for line in stream.readlines():
                    if  line.find('__') != -1: # possible key
                        keys += [k for k in parse_word(line)]
        return set(keys)

    def print_tags(self):
        "Print out template keys"
        for key in self.tmpl_tags():
            print key

    def dir_structure(self):
        "Create dir structure for generated package"
        if  self.debug:
            print "\nCall dir_structure"
        cdir = os.getcwd()
        if  os.path.isdir(self.pname):
            print "Package '%s' already exists in '%s'" \
                    % (self.pname, cdir)
            sys.exit(1)
        else:
            os.makedirs(self.pname)
            os.chdir(self.pname)
        for sdir in self.config.get('dirs'):
            if  not os.path.isdir(sdir):
                os.makedirs(sdir)

    def build_file(self, btmpl=None):
        "Create BuildFile from given template"
        if  self.debug:
            print "\nCall build_file"
        if  btmpl:
            with open('BuildFile.xml', 'w') as stream:
                stream.write(btmpl)
            return
        bname = '%s/%s/BuildFile.tmpl' % (self.tdir, self.tmpl)
        if  self.debug:
            print "Read", bname
        if  not os.path.isfile(bname):
            return
        btmpl = open(bname, 'r').read()
        bfile = ""
        for line in btmpl.split('\n'):
            line = self.parse_etags(line)
            if  not line:
                continue
            bfile += line + '\n'
        with open('BuildFile.xml', 'w') as stream:
            stream.write(bfile)

    def get_tmpl(self, ext):
        "Retrieve template files for given extenstion"
        sdir = '%s/%s' % (self.tdir, self.tmpl)
        sources = [s for s in os.listdir(sdir) \
                if os.path.splitext(s)[-1] == ext]
        return sources

    def parse_etags(self, line):
        """
        Determine either skip or keep given line based on class tags 
        meta-strings
        """
        tmpl_etags = self.tmpl_etags()
        keep_etags = self.config.get('tmpl_etags', [])
        for tag in tmpl_etags:
            if  keep_etags:
                for valid_tag in keep_etags:
                    if  line.find(valid_tag) != -1:
                        line = line.replace(valid_tag, '')
                        return line
            else:
                if  line.find(tag) != -1:
                    line = line.replace(tag, '')
                    line = ''
                    return line
        return line

    def gen_files(self, dst, sources, kwds):
        """
        Generage files at given destination from provided sources and
        replace given tags in template files.
        """
        if  not kwds:
            kwds = {}
        # add author/date/rcsid tags
        subsys = os.getcwd().split('/')[-3]
        kwds.update({'__author__': self.author,
                     '__date__': self.date,
                     '__rcsid__': self.rcsid,
                     '__subsys__': subsys})
        if  self.debug:
            print "Template tags:"
            pprint.pprint(kwds)
        sdir = '%s/%s' % (self.tdir, self.tmpl)
        for src in sources:
            if  self.debug:
                print "Read", src
            name, ext = os.path.splitext(src)
            name = name.replace(self.tmpl, self.pname) + ext
            code = ""
            read_code = False
            with open('%s/%s' % (dst, name), 'w') as stream:
                for line in open('%s/%s' % (sdir, src), 'r').readlines():
                    line = self.parse_etags(line)
                    if  not line:
                        continue
                    if  line.find('#python_begin') != -1:
                        read_code = True
                        continue
                    if  line.find('#python_end') != -1:
                        read_code = False
                    if  read_code:
                        code += line
                    if  code and not read_code:
                        res   = functor(code, kwds, self.debug)
                        stream.write(res)
                        code  = ""
                        continue
                    if  not read_code:
                        for key, val in kwds.items():
                            if  isinstance(val, basestring):
                                line = line.replace(key, val)
                        stream.write(line)

    def python_files(self, kwds):
        "Generate python files"
        if  self.debug:
            print "\n%Call python_files"
        sources = kwds.get('python_files', self.get_tmpl('.py'))
        self.gen_files('python', sources, kwds)

    def cpp_files(self, kwds):
        "Generate C++ files"
        if  self.debug:
            print "\nCall cpp_files"
        sources = kwds.get('cpp_files', 
                self.get_tmpl('.cc') + self.get_tmpl('.cpp'))
        pkgname = self.config.get('pname')
        kwds.update({'__class__': pkgname, '__name__': pkgname})
        self.gen_files('src', sources, kwds)

    def test_files(self, kwds):
        "Generate test files"
        if  self.debug:
            print "\nCall test_files"
        sources = kwds.get('test_files', self.get_tmpl('.tst'))
        self.gen_files('test', sources, kwds)

    def header_files(self, kwds):
        "Generate header files"
        if  self.debug:
            print "\nCall header_files"
        sources = kwds.get('header_files', self.get_tmpl('.h'))
        self.gen_files('interface', sources, kwds)

    def generate(self):
        "Main function"
        if  self.debug:
            print "\nCall generate"
        kwds  = {'__pkgname__': self.pname}
        self.dir_structure()
        ftype = self.config.get('ftype', 'all')
        if  ftype == 'all':
            self.build_file()
            self.python_files(kwds)
            self.cpp_files(kwds)
            self.test_files(kwds)
        else:
            getattr(self, '%s_files' % ftype)(kwds)
        msg = 'New package "%s" of %s type is successfully generated' \
                % (self.config.get('pname'), self.tmpl)
        print msg
