#!/bin/bash

echo "The script [$0]"
echo "The script has basename [`basename $0`]"
echo "The script has dirname [`dirname $0`]"
echo "The current working dir is [`pwd`]"

. ~/.bashrc
echo "COHORTE_HOME =[${COHORTE_HOME}]"

export CURRENTNODE_HOME="`dirname $0`"
echo "CURRENTNODE_HOME =[${CURRENTNODE_HOME}]"

cd "${CURRENTNODE_HOME}"

./run --app-id temper --top-composer true -d