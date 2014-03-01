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

AIR_API_URL="http://vph.cyfronet.pl/api/v1"
SLEEP_TIME=5
PRIVATE_TOKEN="hnbJsUxyG7C-ZWSbJLRg"

APP_SET=`curl -X POST --header "PRIVATE-TOKEN: ${PRIVATE_TOKEN}" ${AIR_API_URL}/appliance_sets?appliance_set_type=development`
APP_SET_ID=`echo $"${APP_SET}" | grep 'id' | awk '{print $2}'`
CONF_TEMP_ID=
APP=`curl -X POST --header "PRIVATE-TOKEN: ${PRIVATE_TOKEN}" ${AIR_API_URL}/appliances?appliance_set_id=${APP_SET_ID}&configuration_template_id=${CONF_TEMP_ID}`

sleep ${SLEEP_TIME}m
VM_STATUS=
if [ ${VM_STATUS} -eq "ACTIVE" ]; then
    echo "Active"
else
    sleep ${SLEEP_TIME}m
    VM_STATUS=
    if [ ${VM_STATUS} -eq "ACTIVE" ]; then
        echo "Active"
    else
        exitoutput="CRITICAL: vm not active, mark as delayed"
        exitstatus=${STATE_CRITICAL}
    fi
fi

curl -X DELETE --header "PRIVATE-TOKEN: ${PRIVATE_TOKEN}" ${AIR_API_URL}/appliance_sets/${APP_SET_ID}

echo ${exitoutput}
exit ${exitstatus}