FROM linuxbrew/linuxbrew

RUN apt-get update && \
    apt-get install -y \
    python3 python3-numpy python3-nose python3-pandas \
    python python-numpy python-nose python-pandas \
    pep8 python-pip python3-pip python-wheel \
    python-sphinx && \
    pip install --upgrade setuptools

RUN brew install gromacs

