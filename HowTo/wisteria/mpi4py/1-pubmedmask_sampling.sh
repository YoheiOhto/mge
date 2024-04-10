#!/bin/sh
#PJM -L rscgrp=regular-o
#PJM -L node=112
#PJM --mpi proc=112
#PJM -g ga97
#PJM -N pubmed_looking

module purge
module load gcc/8.3.1
module load fjmpi/1.2.37

export LD_PRELOAD=/usr/lib/FJSVtcs/ple/lib64/libpmix.so

source ~/.bashrc
pyenv local 3.10.9
source /work/02/ga97/a97006/env/env_o/odyssey_env_mpi4py/bin/activate


mpirun -np 112 python /work/ga97/a97006/nlp_chem_tox/pubmed_mask_samppling/231101_pubmedmask_sampling.py