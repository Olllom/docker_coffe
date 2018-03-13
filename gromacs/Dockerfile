FROM linuxbrew/linuxbrew:1.4.3

#RUN sudo apt-get install -y libssl-dev openssl bzip2

RUN sudo apt-get update
RUN sudo apt-get install -y python3 python3-pip
RUN python3 -m pip install --user virtualenv
#RUN sudo apt-get install -y python-pip
RUN sudo apt-get install -y openbabel

RUN echo "export PATH=/home/linuxbrew/.local/bin:$PATH" > $HOME/.bashrc

RUN brew install gromacs
