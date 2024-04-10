#!/bin/sh
#PJM -L rscgrp=debug-o
#PJM -L node=1
#PJM -g ga97
#PJM -o mpi4py_out.txt
#PJM -e mpi4py_err.txt

module purge
module load gcc/8.3.1
module load fjmpi/1.2.37

export LD_PRELOAD=/usr/lib/FJSVtcs/ple/lib64/libpmix.so

source ~/.bashrc
pyenv local 3.10.4

#python3 -m venv odyssey_env_mpi4py --clear
source odyssey_env_mpi4py/bin/activate

python3 -m pip install --upgrade pip setuptools
#python3 -m pip install mpi4py 