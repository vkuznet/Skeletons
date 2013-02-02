#!/usr/bin/env python
#pylint: disable-msg=c0301,c0103

"""
CMS module unit tests
"""

# system modules
import os
import sys
import shutil
import StringIO
import unittest

# package modules
import Skeletons
from Skeletons.cms import test_cms_environment, generate

class testCMS(unittest.TestCase):
    "A test class"
    def setUp(self):
        "set up"
        # some stuff to init for this class
        self.cdir = os.getcwd()
        self.cmssw_base = '%s/test_tmp' % self.cdir
        os.makedirs(os.path.join(self.cmssw_base, 'src/SubSystem/MyProd/src'))
        os.makedirs(os.path.join(self.cmssw_base, 'src/SubSystem/MyProd/plugins'))

    def tearDown(self):
        "tear down"
        os.chdir(self.cdir)
        shutil.rmtree(self.cmssw_base)

    def test_test_cms_environment(self):
        "Test test_cms_environment function"
        os.chdir(self.cdir)

        expect = False, os.getcwd()
        result = test_cms_environment('EDProducer')
        self.assertEqual(expect, result)

        os.environ['CMSSW_BASE'] = self.cmssw_base

        os.chdir(os.path.join(self.cmssw_base, 'src/SubSystem'))
        expect = 'subsystem', '/SubSystem'
        result = test_cms_environment('EDProducer')
        self.assertEqual(expect, result)

        os.chdir(os.path.join(self.cmssw_base, 'src/SubSystem/MyProd'))
        expect = False, '/SubSystem/MyProd'
        result = test_cms_environment('EDProducer')
        self.assertEqual(expect, result)

        os.chdir(os.path.join(self.cmssw_base, 'src/SubSystem/MyProd/src'))
        expect = 'src', '/SubSystem/MyProd/src'
        result = test_cms_environment('EDProducer')
        self.assertEqual(expect, result)

        os.chdir(os.path.join(self.cmssw_base, 'src/SubSystem/MyProd/plugins'))
        expect = 'plugins', '/SubSystem/MyProd/plugins'
        result = test_cms_environment('EDProducer')
        self.assertEqual(expect, result)

    def test_mkedprod(self):
        "Test creation of EDProducer code"
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        os.chdir(self.cdir)
        os.environ['CMSSW_BASE'] = self.cmssw_base
        test_dir = os.path.join(self.cmssw_base, 'src/SubSystem')
        os.chdir(test_dir)

        sdir   = '/'.join(Skeletons.__file__.split('/')[:-1])
        tdir   = '%s/scripts/mkTemplates' % '/'.join(sdir.split('/')[:-2])
        kwds   = {'author': '', 'tmpl': 'EDProducer', 'pname':'MyPkg',
                  'args': {}, 'debug': False, 'tmpl_dir': tdir}
        generate(kwds)
        dirs   = os.listdir(test_dir)
        expect = True
        result = 'MyPkg' in dirs
        self.assertEqual(expect, result)

        sys.stdout = old_stdout

#
# main
#
if __name__ == '__main__':
    unittest.main()
