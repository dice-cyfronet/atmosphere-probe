#!/bin/sh

set -e
#set -x

# Return codes:

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

# Arguments:

if [ $# -ne 3 ]; then
    exit ${STATE_UNKNOWN}
fi

DIRECTORY=$1
WARNLEVEL=$2
CRITLEVEL=$3

# Get current file count:

FCOUNT=`ls -l ${DIRECTORY} |grep -v tot* |wc -l`

if [ ${FCOUNT} -lt ${WARNLEVEL} ]; then
    echo "OK: ${FCOUNT} items in ${DIRECTORY}|files=${FCOUNT}"
    exit ${STATE_OK}
fi

if [ ${FCOUNT} -gt ${CRITLEVEL} ]; then
    echo "CRITICAL: ${FCOUNT} items in ${DIRECTORY}|files=${FCOUNT}"
    exit ${STATE_CRITICAL}
fi

if [ ${FCOUNT} -gt ${WARNLEVEL} ]; then
    echo "WARNING: ${FCOUNT} items in ${DIRECTORY}|files=${FCOUNT}"
    exit ${STATE_WARNING}
fi
