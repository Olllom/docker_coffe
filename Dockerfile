FROM linuxbrew/linuxbrew

RUN sudo apt-get update
RUN sudo apt-get install -y \
	python-pip \
	python-dev \
	python3-pip \
	python3-dev \
	build-essential \
	python-numpy \
	cython \
	python-scipy



RUN brew install gromacs

