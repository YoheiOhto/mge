#!/bin/sh
#PJM -L rscgrp=debug-a
#PJM -g gg17
#PJM -L gpu=1
#PJM -e ohto_test_env_err.txt
#PJM -o ohto_test_env_out.txt

# module load
module load cuda/11.3
module load cudnn/8.2.0
module load gcc/8.3.1
module load python/3.11.7

# Make env (mvenv)
python3 -m venv ohto_test_a --clear
source ohto_test_a/bin/activate

pip3 install --upgrade pip

pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
