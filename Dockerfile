FROM linuxbrew/linuxbrew

RUN brew install python python3.5

RUN 'export PATH="/home/linuxbrew/.linuxbrew/opt/python/libexec/bin:$PATH"' >> /home/linuxbrew/.bashrc
RUN 'export PYTHONPATH=/home/linuxbrew/.linuxbrew/lib/python2.7/site-packages:$PYTHONPATH' >> /home/linuxbrew/.bashrc
RUN 'export PYTHONPATH=/home/linuxbrew/.linuxbrew/lib/python3.5/site-packages:$PYTHONPATH' >> /home/linuxbrew/.bashrc

RUN brew install gromacs
