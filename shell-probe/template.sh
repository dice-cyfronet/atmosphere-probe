#!/bin/sh

set -e
#set -x

# Return codes:

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

# Arguments:

if [ $# -ne 0 ]; then
    exit ${STATE_UNKNOWN}
fi

TEST=0

if [ ${TEST} -eq 0 ]; then
    exit ${STATE_OK}
fi

if [ ${TEST} -eq 1 ]; then
    exit ${STATE_WARNING}
fi

if [ ${TEST} -eq 2 ]; then
    exit ${STATE_CRITICAL}
fi

if [ ${TEST} -eq 3 ]; then
    exit ${STATE_UNKNOWN}
fi