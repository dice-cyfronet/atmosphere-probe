#!/bin/bash

export __dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export __dir="$( dirname ${__dir} )"

command -v virtualenv >/dev/null 2>&1 || { echo >&2 "I require \`virtualenv\` but it's not installed. Aborting."; exit 1; }

if [ ! -d ${__dir}/__envi ]
then
    virtualenv ${__dir}/__envi
fi

. ${__dir}/__envi/bin/activate

set -x

${__dir}/__envi/bin/pip install --upgrade distribute
${__dir}/__envi/bin/pip install --upgrade -r ${__dir}/requirements.txt

if [ ! -f ${__dir}/etc/secure.ini ]
then
    echo the file does not exist
    cp ${__dir}/etc/secure-example.ini ${__dir}/etc/secure.ini
    set +x
    read -p "Enter proxy certificate path: " proxy_path
    read -p "Enter configuration appliance template ID (like: 371): " conf_at_id
    set -x
    sed -i "s/X509_PROXY_FILE = proxypath/X509_PROXY_FILE = ${proxy_path}/g" ${__dir}/etc/secure.ini
    sed -i "s/CONF_AT_ID = id/CONF_AT_ID = ${conf_at_id}/g" ${__dir}/etc/secure.ini
fi

