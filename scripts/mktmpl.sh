#!/bin/sh
#
# this is a base script which should be used by CMS mk* scripts
# it requires the following variables
# cmd: the name of the mk script, e.g. mkedprod
# tmpl: the name of mk template, e.g. EDProducer
# help_examples: the appropriate help message
#
# find out where Skeleton is installed on a system
sroot=`python -c "import Skeletons; print '/'.join(Skeletons.__file__.split('/')[:-1])"`
# run actual script
ecmd="echo"
if  [ `uname` == "Linux" ]; then
    ecmd="echo -e"
fi
if  [ -z "$1" ] || [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ "$1" == "-help" ]; then
    $ecmd "$cmd generates CMS $tmpl code"
    $ecmd "Usage: $cmd [options]"
    $ecmd "Options:"
    $ecmd "\t-h, --help           show this help message and exit"
    $ecmd "\t--debug              debug output"
    $ecmd "\t--author=AUTHOR      specify author name"
    $ecmd "\t--keep-etags=KETAGS  list examples tags which should be kept in generate"
    $ecmd "\t                     code, e.g. --keep-etags='@example_trac'"
    $ecmd "\t--tags               list template tags"
    $ecmd "\t--etags              list template example tags"
    $ecmd $examples
    exit
fi
tdir=`echo $0 | sed "s,/$cmd,,g"`
opts="--tmpl=$tmpl --tdir=/$tdir/mkTemplates"
base=`env | grep ^CMSSW_BASE=`
cmssw=`echo "$base/src" | sed -e "s,//,/,g" -e "s,CMSSW_BASE=,,g"`
ldir=`echo $PWD | awk '{z=split($0,a,"/"); print a[z]}'`
error()
{
    echo ""
    echo "Packages must be created in a 'subsystem'."
    echo "Please set your CMSSW environment and go to $CMSSW_BASE/src"
    echo "Create or choose directory from there and then "
    echo "run the script from that directory"
    exit
}
if  [ -n "$ldir" ]; then
    # check if we're at any existing directory
    if [ -d "$ldir" ]; then
        error
    else # check subsysytem
        if [ -d "../../$ldir" ]; then
            # we're within subsystem level
            error
        fi
        sdir=`echo "$ldir" | egrep "src$|plugin$"`
        if  [ "$sdir" == "$ldir" ]; then
            # we're within subsystem/src level
            opts="$opts --ftype=cpp"
        fi
    fi
elif [ -z "$ldir" ] || [ ! -d "../$ldir" ]; then # check subsystem
    error
fi
python $sroot/main.py $opts ${1+"$@"}
