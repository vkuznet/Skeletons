#-*- coding: utf-8 -*-
#pylint: disable-msg=W0122,R0914

"""
File       : utils.py
Author     : Valentin Kuznetsov <vkuznet@gmail.com>
Description: Utilities module
"""

# system modules
import os
import re
import sys
import pwd
import pprint
import subprocess

# template tag pattern
TAG = re.compile(r'[a-zA-Z0-9]')

def parse_word(word):
    "Parse word which contas double underscore tag"
    output = set()
    words  = word.split()
    for idx in xrange(0, len(words)):
        pat = words[idx]
        if  pat and len(pat) > 4 and pat[:2] == '__': # we found enclosure
            tag = pat[2:pat.rfind('__')]
            if  tag.find('__') != -1: # another pattern
                for item in tag.split('__'):
                    if  TAG.match(item):
                        output.add('__%s__' % item)
            else:
                output.add('__%s__' % tag)
    return output

def test_env(tdir, tmpl):
    """
    Test user environment, look-up if user has run cmsenv, otherwise
    provide meaningful error message back to the user.
    """
    if  not tdir or not os.path.isdir(tdir):
        print "Unable to access template dir: %s" % tdir
        sys.exit(1)
    if  not os.listdir(tdir):
        print "No template files found in template dir %s" % tdir
        sys.exit(0)
    if  not tmpl:
        msg  = "No template type is provided, "
        msg += "see available templates via --templates option"
        print msg
        sys.exit(1)

def functor(code, kwds, debug=0):
    """
    Auto-generate and execute function with given code and configuration
    For details of compile/exec/eval see
    http://lucumr.pocoo.org/2011/2/1/exec-in-python/
    """
    args  = []
    for key, val in kwds.items():
        if  isinstance(val, basestring):
            arg = '%s="%s"' % (key, val)
        elif isinstance(val, list):
            arg = '%s=%s' % (key, val)
        else:
            msg = 'Unsupported data type "%s" <%s>' % (val, type(val)) 
            raise Exception(msg)
        args.append(arg)
    func  = '\nimport sys'
    func += '\nimport StringIO'
    func += "\ndef func(%s):\n" % ','.join(args)
    func += code
    func += """
def capture():
    "Capture snippet printous"
    old_stdout = sys.stdout
    sys.stdout = StringIO.StringIO()
    func()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out\n
capture()\n"""
    if  debug:
        print "\n### generated code\n"
        print func
    # compile python code as exec statement
    obj   = compile(func, '<string>', 'exec')
    # define execution namespace
    namespace = {}
    # execute compiled python code in given namespace
    exec obj in namespace
    # located generated function object, run it and return its results
    return namespace['capture']()

def get_user_info(ainput=None):
    "Return user name and office location, based on UNIX finger"
    if  ainput:
        return ainput
    pwdstr = pwd.getpwnam(os.getlogin())
    author = pwdstr.pw_gecos
    return author

def get_code_generator(kwds):
    """
    Code generator function, parse user arguments, load and
    return appropriate template generator module.
    """
    debug = kwds.get('debug', None)
    if  debug:
        print "Configuration:"
        pprint.pprint(kwds)
    try:
        klass  = kwds.get('tmpl')
        mname  = 'Skeletons.%s' % klass.lower()
        module = __import__(mname, fromlist=[klass])
    except ImportError as err:
        klass  = 'AbstractPkg'
        module = __import__('Skeletons.pkg', fromlist=[klass])
        if  debug:
            print "%s, will use %s" % (str(err), klass)
    obj = getattr(module, klass)(kwds)
    return obj
