============
docker_coffe
============

Dockerfiles and scripts for running the continuous integration framework for coffe_ locally.

.. _coffe: https://gitlab.com/olllom/coffe

Each docker image has python and one molecular simulation engine installed (Gromacs, Amber, CHARMM).
The Dockerfiles are located in the subfolders of this github repository.
The Docker images are publically available on my docker hub_ page.
Pushing to the present repository automatically invokes a build on docker hub.

.. _hub: https://hub.docker.com/r/olllom/


Requirements:

- docker_
- coffe_
- Click (installed automatically by setup.py)
- docker python (installed automatically by setup.py)

.. _docker: https://docker.com
.. _coffe: https://gitlab.com/olllom/coffe

Installation:

- ``python setup.py``


Usage:

- see ``docoffe -h``


Note:

When ``docoffe`` is executed for the first time, it takes very long to execute,
(four docker images, each one almost 1 GB large, have to be downloaded in the process).
The boe