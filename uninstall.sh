#!/bin/bash

set -x

export __DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export virtenv_dir=${__DIR}/virtenv
rm -rf ${virtenv_dir}