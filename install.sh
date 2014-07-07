#!/bin/bash

set -x

export __DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -f ${__DIR}/secure.ini ]
then
    echo the file does not exist
    cp ${__DIR}/secure-example.ini ${__DIR}/secure.ini
    set +x
    read -p "Enter private token: " token
    read -p "Enter configuration appliance template ID (like: 371): " conf_at_id
    set -x
    sed -i "s/API_PRIVATE_TOKEN = token/API_PRIVATE_TOKEN = ${token}/g" ${__DIR}/secure.ini
    sed -i "s/CONF_AT_ID = id/CONF_AT_ID = ${conf_at_id}/g" ${__DIR}/secure.ini
fi

export virtenv_dir=${__DIR}/virtenv
mkdir -p ${virtenv_dir}

curl -L -o ${virtenv_dir}/virtualenv.py https://raw.githubusercontent.com/pypa/virtualenv/master/virtualenv.py
python ${virtenv_dir}/virtualenv.py ${virtenv_dir}/enviroment --no-setuptools
. ${virtenv_dir}/enviroment/bin/activate

wget -O ${virtenv_dir}/simplejson.zip --no-check-certificate https://github.com/simplejson/simplejson/archive/master.zip
unzip ${virtenv_dir}/simplejson.zip -d ${virtenv_dir}/
pushd ${virtenv_dir}/simplejson-master
${virtenv_dir}/enviroment/bin/python setup.py install
popd

wget -O ${virtenv_dir}/air-python.zip --no-check-certificate https://gitlab.dev.cyfronet.pl/paoolo/air-python/repository/archive.zip
unzip ${virtenv_dir}/air-python.zip -d ${virtenv_dir}/
pushd ${virtenv_dir}/air-python.git
${virtenv_dir}/enviroment/bin/python setup.py install
popd

wget -O ${virtenv_dir}/paramiko.zip --no-check-certificate https://github.com/paramiko/paramiko/archive/master.zip
unzip ${virtenv_dir}/paramiko.zip -d ${virtenv_dir}/
pushd ${virtenv_dir}/paramiko-master
${virtenv_dir}/enviroment/bin/python setup.py install
popd

wget -O ${virtenv_dir}/ecdsa.zip --no-check-certificate https://github.com/warner/python-ecdsa/archive/master.zip
unzip ${virtenv_dir}/ecdsa.zip -d ${virtenv_dir}/
pushd ${virtenv_dir}/python-ecdsa-master
${virtenv_dir}/enviroment/bin/python setup.py install
popd

wget -O ${virtenv_dir}/crypto.tar.gz --no-check-certificate https://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.6.1.tar.gz
pushd ${virtenv_dir}
tar zxvf ${virtenv_dir}/crypto.tar.gz
pushd ${virtenv_dir}/pycrypto-2.6.1
${virtenv_dir}/enviroment/bin/python setup.py install
popd
popd

