#!/bin/bash

set -x

export __DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -f ${__DIR}/secure.ini ]
then
    echo the file does not exist
    cp ${__DIR}/secure-example.ini ${__DIR}/secure.ini
    set +x
    read -p "Enter private token: " token
    read -p "Enter configuration appliance template ID: " conf_at_id
    set -x
    sed -i "s/API_PRIVATE_TOKEN = token/API_PRIVATE_TOKEN = ${token}/g" ${__DIR}/secure.ini
    sed -i "s/CONF_AT_ID = id/CONF_AT_ID = ${conf_at_id}/g" ${__DIR}/secure.ini
fi

export virtenv_dir=${__DIR}/virtenv
mkdir -p ${virtenv_dir}

curl -L -o ${virtenv_dir}/virtualenv.py https://raw.githubusercontent.com/pypa/virtualenv/master/virtualenv.py
python ${virtenv_dir}/virtualenv.py ${virtenv_dir}/enviroment --no-setuptools
. ${virtenv_dir}/enviroment/bin/activate

GIT_SSL_NO_VERIFY=true git clone https://github.com/simplejson/simplejson.git ${virtenv_dir}/simplejson
pushd ${virtenv_dir}/simplejson
${virtenv_dir}/enviroment/bin/python setup.py install
popd

GIT_SSL_NO_VERIFY=true git clone https://gitlab.dev.cyfronet.pl/paoolo/air-python.git ${virtenv_dir}/air-python
pushd ${virtenv_dir}/air-python
${virtenv_dir}/enviroment/bin/python setup.py install
popd

GIT_SSL_NO_VERIFY=true git clone https://github.com/pexpect/pexpect.git ${virtenv_dir}/pexpect
pushd ${virtenv_dir}/pexpect
${virtenv_dir}/enviroment/bin/python setup.py install
popd