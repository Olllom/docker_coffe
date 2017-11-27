FROM fourplusone/docker-gromacs

#RUN brew install pyenv
#RUN pyenv install 3.5.0
#RUN pyenv install 2.7.10

RUN apt-get update
RUN apt-get -y install python-pip python3-pip virtualenv

#RUN 'export PATH="/home/linuxbrew/.linuxbrew/opt/python/libexec/bin:$PATH"' >> /home/linuxbrew/.bashrc
#RUN 'export PYTHONPATH=/home/linuxbrew/.linuxbrew/lib/python2.7/site-packages:$PYTHONPATH' >> /home/linuxbrew/.bashrc
#RUN 'export PYTHONPATH=/home/linuxbrew/.linuxbrew/lib/python3.5/site-packages:$PYTHONPATH' >> /home/linuxbrew/.bashrc

#RUN brew install gromacs
