#!/usr/bin/env python

"""
Standard python setup.py file for Skeletons package

To build     : python setup.py build
To install   : python setup.py install --prefix=<some dir>
To clean     : python setup.py clean
To build doc : python setup.py doc
To run tests : python setup.py test

"""
__author__ = "Valentin Kuznetsov"

import os
import sys
import shutil
import subprocess
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.errors import DistutilsPlatformError, DistutilsExecError
from distutils.core import Extension
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.install import INSTALL_SCHEMES

# add some path which will define the version,
# e.g. it can be done in DataProvider/__init__.py
sys.path.append(os.path.join(os.getcwd(), 'python'))
try:
    from DataProvider import version as dp_version
except:
    dp_version = 'development' # some default

required_python_version = '2.6'
if sys.platform == 'win32' and sys.version_info > (2, 6):
   # 2.6's distutils.msvc9compiler can raise an IOError when failing to
   # find the compiler
   build_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError,
                 IOError)
else:
   build_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

class TestCommand(Command):
    "Class to handle unit tests"
    user_options = [ ]

    def initialize_options(self):
        "Init method"
        self._dir = os.getcwd()

    def finalize_options(self):
        "Finalize method"
        pass

    def run(self):
        "Finds all the tests modules in tests/, and runs them"
        # list of files to exclude,
        # e.g. [pjoin(self._dir, 'tests', 'exclude_t.py')]
        exclude = []
        # list of test files
        testfiles = []
        for tname in glob(pjoin(self._dir, 'tests', '*_t.py')):
            if  not tname.endswith('__init__.py') and \
                tname not in exclude:
                testfiles.append('.'.join(
                    ['tests', splitext(basename(tname))[0]])
                )
        testfiles.sort()
        try:
            tests = TestLoader().loadTestsFromNames(testfiles)
        except:
            print "Fail to load unit tests", testfiles
            raise
        test = TextTestRunner(verbosity = 2)
        test.run(tests)
        # run integration tests
        print "run integration tests"
        cdir = os.getcwd()
        base = os.path.join(os.getcwd(), 'int_tests')
        wdir = os.path.join(base, 'src/SubSystem')
        sdir = os.path.join(os.getcwd(), 'scripts')
        tdir = os.path.join(sdir, 'mkTemplates')
        os.environ['CMSSW_BASE'] = base
        if  os.path.isdir(base):
            shutil.rmtree(base)
        os.makedirs(wdir)
        os.chdir(wdir)
        for pkg in os.listdir(tdir):
            test_pkg = 'My%s' % pkg
            script = find_script(sdir, pkg)
            if  script.find('mktmpl') != -1:
                cmd = '%s/%s --name=%s' % (sdir, script, test_pkg)
            else:
                cmd = '%s/%s %s' % (sdir, script, test_pkg)
            print cmd
            subprocess.call(cmd, shell=True)
            if  pkg in ['Record', 'Skeleton']:
                for fname in os.listdir(os.getcwd()):
                    print fname
                    os.remove(fname)
            else:
                for root, dirs, files in os.walk(test_pkg):
                    print root
                    for fname in files:
                        print '   ', fname
                shutil.rmtree(test_pkg)
        if  os.path.isdir(base):
            shutil.rmtree(base)
        os.chdir(cdir)

def find_script(sdir, pkg):
    "Find CMS mk-script for given template package"
    scripts = os.listdir(sdir)
    for idx in range(4, 1, -1):
        for scr in scripts:
            if  scr[:idx+2] == 'mk%s' % pkg.lower()[:idx]:
                return scr
    return "mktmpl --tmpl=%s" % pkg

class CleanCommand(Command):
    "Class which clean-up all pyc files"
    user_options = [ ]

    def initialize_options(self):
        "Init method"
        self._clean_me = [ ]
        for root, dirs, files in os.walk('.'):
            for fname in files:
                if  fname.endswith('.pyc') or fname. endswith('.py~') or \
                    fname.endswith('.rst~'):
                    self._clean_me.append(pjoin(root, fname))
            for dname in dirs:
                if  dname == 'build' or dname == '_build':
                    self._clean_me.append(pjoin(root, dname))

    def finalize_options(self):
        "Finalize method"
        pass

    def run(self):
        "Run method"
        for clean_me in self._clean_me:
            try:
                if  os.path.isdir(clean_me):
                    shutil.rmtree(clean_me)
                else:
                    os.unlink(clean_me)
            except:
                pass

class DocCommand(Command):
    "Class which build documentation"
    user_options = [ ]

    def initialize_options(self):
        "Init method"
        pass

    def finalize_options(self):
        "Finalize method"
        pass

    def run(self):
        "Run method"
        cdir = os.getcwd()
        os.chdir(os.path.join(os.path.join(cdir, 'doc'), 'sphinx'))
        os.environ['PYTHONPATH'] = os.path.join(cdir, 'python')
        subprocess.call('make html', shell=True)
        subprocess.call('make man', shell=True)
        os.chdir(cdir)

class BuildExtCommand(build_ext):
    "Build C-extentions"

    def initialize_options(self):
        "Init method"
        pass

    def finalize_options(self):
        "Finalize method"
        pass

    def run(self):
        "Run method"
        try:
            build_ext.run(self)
        except DistutilsPlatformError as exp:
            print exp
            print "Could not compile extension module"

    def build_extension(self, ext):
        "Build extension method"
        try:
            build_ext.build_extension(self, ext)
        except build_errors:
            print "Could not compile %s" % ext.name

def dirwalk(relativedir):
    "Walk a directory tree and look-up for __init__.py files"
    idir = os.path.join(os.getcwd(), relativedir)
    for fname in os.listdir(idir):
        fullpath = os.path.join(idir, fname)
        if  os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for subdir in dirwalk(fullpath):  # recurse into subdir
                yield subdir
        else:
            initdir, initfile = os.path.split(fullpath)
            if  initfile == '__init__.py':
                yield initdir

def find_packages(relativedir):
    "Find list of packages in a given dir"
    packages = []
    for idir in dirwalk(relativedir):
        package = idir.replace(os.getcwd() + '/', '')
        package = package.replace(relativedir + '/', '')
        package = package.replace('/', '.')
        packages.append(package)
    return packages

def datafiles(idir, recursive=True):
    "Return list of data files in provided relative dir"
    files = []
    if  idir[0] != '/':
        idir = os.path.join(os.getcwd(), idir)
    for dirname, dirnames, filenames in os.walk(idir):
        if  dirname != idir:
            continue
        if  recursive:
            for subdirname in dirnames:
                files.append(os.path.join(dirname, subdirname))
        for filename in filenames:
            if  filename[-1] == '~':
                continue
            files.append(os.path.join(dirname, filename))
    return files

def install_prefix(idir=None):
    "Return install prefix"
    inst_prefix = sys.prefix
    for arg in sys.argv:
        if  arg.startswith('--prefix='):
            inst_prefix = os.path.expandvars(arg.replace('--prefix=', ''))
            break
    if  idir:
        return os.path.join(inst_prefix, idir)
    return inst_prefix

def main():
    "Main function"
    version      = dp_version
    name         = "Skeletons"
    description  = "Skeletons description"
    url          = "Skeletons URL"
    readme       = "Skeletons readme"
    author       = "Valentin Kuznetsov",
    author_email = "<Valentin Kuznetsov email [dot] com>",
    keywords     = ["Skeletons"]
    package_dir  = {'Skeletons': 'python/Skeletons'}
    packages     = find_packages('python')
    extentions   = [] # list your extensions here
    data_files   = [] # list of tuples whose entries are (dir, [data_files])
    data_files   = [(install_prefix('etc'), datafiles('etc')),
                    (install_prefix('scripts'), datafiles('scripts'))
                   ]
    cms_license  = "Skeletons license"
    classifiers  = [
        "Development Status :: 3 - Production/Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Skeletons License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: General"
    ]

    if  sys.version < required_python_version:
        msg = "I'm sorry, but %s %s requires Python %s or later."
        print msg % (name, version, required_python_version)
        sys.exit(1)

    # set default location for "data_files" to
    # platform specific "site-packages" location
    for scheme in INSTALL_SCHEMES.values():
        scheme['data'] = scheme['purelib']

    setup(
        name                 = name,
        version              = version,
        description          = description,
        long_description     = readme,
        keywords             = keywords,
        packages             = packages,
        package_dir          = package_dir,
        data_files           = data_files,
        scripts              = datafiles('bin'),
        requires             = ['python (>=2.6)'],
        classifiers          = classifiers,
        ext_modules          = extentions,
        cmdclass             = {'build_ext': BuildExtCommand,
                                'test': TestCommand,
                                'clean': CleanCommand,
                                'doc': DocCommand},
        author               = author,
        author_email         = author_email,
        url                  = url,
        license              = cms_license,
    )

if  __name__ == "__main__":
    main()
