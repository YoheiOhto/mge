FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04
COPY requirements.txt /requirements.txt
ARG PYTHON_VER
ENV PYTHON_VER=$PYTHON_VER
WORKDIR /workspace
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN apt-get update
RUN apt-get install -y --fix-missing curl \ 
  vim \ 
  less \
  git \
  tzdata
RUN apt-get install -y nodejs 
RUN apt-get install -y npm
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*
RUN apt update && \
    apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils libffi-dev liblzma-dev &&\
    apt install -y libxml2-dev libboost-all-dev libomp-dev zlib1g-dev libeigen3-dev libcairo2-dev cmake swig
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
  echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
  . /root/.bashrc && \
  pyenv install ${PYTHON_VER} && \
  pyenv global ${PYTHON_VER} && \
  cd /opt && \
  python3 -m venv pip-env && \
  . /opt/pip-env/bin/activate && \
  pip install --upgrade pip && \
  pip install --upgrade setuptools && \
  pip install --no-cache-dir -r /requirements.txt \
  flake8 \
  autopep8