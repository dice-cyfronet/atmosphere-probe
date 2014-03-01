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

IMAGE_ID=$1
IMAGE_ID="5d5a4308-1e6b-4871-a45a-73927f6c9887"

SLEEP_TIME=$2
SLEEP_TIME=5


VM_NAME=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 40 | head -n 1`
NOVA_BOOT=`nova boot --image ${IMAGE_ID} --flavor m1.tiny ${VM_NAME}`
VM_ID=`echo $"${NOVA_BOOT}" | grep '| id' | awk '{print $4}'`

sleep ${SLEEP_TIME}m
VM_STATUS=`nova show ${VM_ID} | grep status | awk '{print $4}'`
if [ ${VM_STATUS} -eq "ACTIVE" ]; then
    echo "Active"
else
    sleep ${SLEEP_TIME}m
    VM_STATUS=`nova show ${VM_ID} | grep status | awk '{print $4}'`
    if [ ${VM_STATUS} -eq "ACTIVE" ]; then
        echo "Active"
    else
        exitoutput="CRITICAL: vm not active, mark as delayed"
        exitstatus=${STATE_CRITICAL}
    fi
fi

VM_STATUS=`nova show ${VM_ID} | grep status | awk '{print $4}'`
VM_IP=`nova show ${VM_ID} | grep network | awk '{print $5}'`

echo ${exitoutput}
exit ${exitstatus}