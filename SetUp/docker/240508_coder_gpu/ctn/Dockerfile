# === description ===
# base dockerfile for code-server in docker

# === composition ===
# 1. desired environment
# 2. code-server setting

# === history ===
# 240430 start writing by ohto yohei

# 1. desired environment
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# linux setting
# RUN mkdir /workspace
WORKDIR /workspace
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ARG PYTHON_VER
ENV PYTHON_VER=$PYTHON_VER
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

RUN apt-get update \
  && apt-get install -y locales \
  && locale-gen ja_JP.UTF-8 \
  && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc

# python setting
COPY requirements.txt /requirements.txt
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
  python3 -m venv coder-gpu && \
  . /opt/pip-env/bin/activate && \
  pip install --upgrade pip && \
  pip install --upgrade setuptools && \
  pip install ipykernel ipython && \
  ipython kernel install --user --name=coder-gpu --display-name=coder-gpu && \
  pip install --no-cache-dir -r /requirements.txt \
  flake8 \
  autopep8

# 2. code-server setting
# RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN code-server \
  --install-extension ms-python.python \
  --install-extension ms-ceintl.vscode-language-pack-ja
