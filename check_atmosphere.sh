#!/bin/bash

export __DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export virtenv_dir=${__DIR}/virtenv
. ${virtenv_dir}/enviroment/bin/activate

${virtenv_dir}/enviroment/bin/python check_atmosphere.py