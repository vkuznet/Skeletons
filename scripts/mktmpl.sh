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
if  [ -z "$1" ] || [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ "$1" == "-help" ]; then
    echo "$cmd generates CMS $tmpl code"
    echo "Usage: $cmd [options]"
    echo "Options:"
    echo "\t-h, --help           show this help message and exit"
    echo "\t--debug              debug output"
    echo "\t--author=AUTHOR      specify author name"
    echo "\t--keep-etags=KETAGS  list examples tags which should be kept in generate"
    echo "\t                     code, e.g. --keep-etags='@example_trac'"
    echo "\t--tags               list template tags"
    echo "\t--etags              list template example tags"
    echo $examples
    exit
fi
tdir=`echo $0 | sed "s,/$cmd,,g"`
opts="--tmpl=$tmpl --tdir=/$tdir/mkTemplates"
base=`env | grep CMSSW_BASE`
cmssw=`echo "$base/src" | sed -e "s,//,/,g" -e "s,CMSSW_BASE=,,g"`
ldir=`echo $PWD | sed "s,$cmssw,,g"`
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
        sdir=`echo "$ldir" | grep "/src$"`
        if [ -d "../../../$ldir" ] && [ "$sdir" == "$ldir" ]; then
            # we're within subsystem/src level
            opts="$opts --ftype=cpp"
        fi
    fi
elif [ -z "$ldir" ] || [ ! -d "../$ldir" ]; then # check subsystem
    error
fi
python $sroot/main.py $opts ${1+"$@"}
