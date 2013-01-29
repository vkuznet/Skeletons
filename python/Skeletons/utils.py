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
    func  = "\ndef func(%s):\n" % ','.join(args)
    func += code
    func += 'func()\n'
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
    return namespace['func']()

def get_user_info(ainput):
    "Return user name and office location, based on UNIX finger"
    if  ainput:
        return ainput, ''
    cmd = "finger `whoami`"
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    author = os.getlogin()
    office = ''
    for line in res.stdout.read().split('\n'):
        if  line.find('Name:') != -1:
            author = line.split('Name:')[-1].strip()
        if  line.find('Office:') != -1:
            office = line.split('Office:')[-1].strip()
    return author, office
