#!/bin/bash

UPSIDE_HOME=$(pwd)

cat > source.sh << EOF
export UPSIDE_HOME=$UPSIDE_HOME
source \$UPSIDE_HOME/.venv/bin/activate
export PATH=\$UPSIDE_HOME/obj:\$PATH
export PYTHONPATH=\$UPSIDE_HOME/py:\$PYTHONPATH
EOF

source source.sh

rm -rf obj/*
cd obj

cmake ../src/
make
