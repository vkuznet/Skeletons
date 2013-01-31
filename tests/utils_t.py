#!/usr/bin/env python
#pylint: disable-msg=c0301,c0103

"""
Skeletons.utils unit tests
"""

# system modules
import sys
import unittest

# package modules
from Skeletons.utils import parse_word, functor, get_code_generator

class testUtils(unittest.TestCase):
    "A test class"
    def setUp(self):
        "set up"
        # some stuff to init for this class
        pass

    def test_parse_word(self):
        "Test parse_word function"
        sts = "sdlkfj __class__::Bla"
        result = parse_word(sts)
        expect = set(["__class__"])
        self.assertEqual(expect, result)

    def test_functor(self):
        "Test functor function"
        snippet = """
#python_begin
    for i in __data__:
        print i
#python_end
        """
        data   = range(5)
        result = functor(snippet, {'__data__':data})
        expect = '\n'.join([str(i) for i in data]) + '\n'
        self.assertEqual(expect, result)

    def test_get_code_generator(self):
        "Test get_code_generator function"
        kwds   = {'author': '', 'tmpl': 'c++11', 'pname':'MyProd',
                  'args': {}, 'debug': False, 'tmpl_dir': ''}
        obj = get_code_generator(kwds)
        result = str(type(obj))
        expect = """<class 'Skeletons.pkg.AbstractPkg'>"""
        self.assertEqual(expect, result)

        kwds   = {'author': '', 'tmpl': 'TSelector', 'pname':'MyProd',
                  'args': {}, 'debug': False, 'tmpl_dir': ''}
        obj = get_code_generator(kwds)
        result = str(type(obj))
        expect = """<class 'Skeletons.tselector.TSelector'>"""
        self.assertEqual(expect, result)
#
# main
#
if __name__ == '__main__':
    unittest.main()
