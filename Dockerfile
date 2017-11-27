FROM linuxbrew/linuxbrew

#RUN sudo apt-get install -y libssl-dev openssl bzip2
RUN sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev
RUN brew update
RUN brew install readline 
RUN brew install pyenv
#RUN CFLAGS="-I$(brew --prefix openssl)/include" \
#    LDFLAGS="-L$(brew --prefix openssl)/lib" \
RUN pyenv install -v 3.5.4

#RUN CFLAGS="-I$(brew --prefix openssl)/include" \
#    LDFLAGS="-L$(brew --prefix openssl)/lib" \
RUN pyenv install -v 2.7.10

#RUN 'export PATH="/home/linuxbrew/.linuxbrew/opt/python/libexec/bin:$PATH"' >> /home/linuxbrew/.bashrc
#RUN 'export PYTHONPATH=/home/linuxbrew/.linuxbrew/lib/python2.7/site-packages:$PYTHONPATH' >> /home/linuxbrew/.bashrc
#RUN 'export PYTHONPATH=/home/linuxbrew/.linuxbrew/lib/python3.5/site-packages:$PYTHONPATH' >> /home/linuxbrew/.bashrc

RUN brew install gromacs
