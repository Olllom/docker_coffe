#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulates the continuous integration framework on a local machine.
"""

from __future__ import absolute_import, division, print_function

import subprocess as sp
import os
import sys
import docker
import click
import tarfile as tf
from io import BytesIO


IMAGES = {
    "no": "olllom/coffeci-no",
    "chm": "olllom/coffeci-chm",
    "amb": "olllom/coffeci-amb",
    "gmx": "olllom/coffeci-gmx",
}


def check_docker():
    """Check if docker is installed. Exit program with error message otherwise.
    """
    which = sp.Popen("which docker".split(), stdout=sp.PIPE, stderr=sp.PIPE)
    out, _ = which.communicate()
    if len(out) == 0:
        print("Fatal error: Docker is not installed on your machine. Exiting.")
        sys.exit(1)


class InParentDir(object):
    """
    A helper class to execute the tar-ing in the parent directory
    """
    def __init__(self, path):
        self.orig = os.path.abspath(os.getcwd())
        if os.path.isfile(path):
            self.work_dir = os.path.dirname(path)
        else:
            self.work_dir = os.path.normpath(os.path.join(path, os.path.pardir))
        os.chdir(self.work_dir)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self.orig)


def autodetect_coffe():
    try:
        import coffe
        coffedir = os.path.normpath(os.path.join(os.path.dirname(coffe.__file__), os.path.pardir))
        print("Found coffe at {}".format(coffedir))
        return coffedir
    except:
        print ("Did not find coffe. Exiting.")
        sys.exit(1)


def extract_yml_cmds(coffedir, container_name):
    yml = os.path.join(coffedir, ".gitlab-ci.yml")
    assert os.path.isfile(yml)
    result = []
    # make sure all images are defined in yml file
    for k in IMAGES:
        with open(yml, "r") as f:
            assert any(IMAGES[k] in l for l in f), "Error: Image {} not found in .gitlab-ci.yml".format(IMAGES[k])
    # extract relevant lines of script
    with open(yml, "r") as f:
        right_section = False
        in_right_script = False
        for l in f:
            line = l.strip()
            if right_section:
                if in_right_script and line.startswith("-"):
                    line = line[1:].strip()
                    result += [line]
                    continue
                elif line.startswith("script"):
                    in_right_script = True
                    continue
                else:
                    return result
            elif "image" in line and container_name in line:
                right_section = True
                continue
            else:
                continue


class InteractiveDockerContainer(object):
    """A customized wrapper to the docker.Container class
    """
    def __init__(self, container_name):
        assert container_name in IMAGES
        self.image = IMAGES[container_name]
        self.name = container_name
        print("Create container {}".format(self.name))
        client = docker.from_env()
        self.container = client.containers.run(self.image, "/bin/bash", detach=True, tty=True)
        self.container.rename(self.name)

    def __call__(self, cmd, workdir=None, environment=[]):
        """Run a command in workdir, print output and return the result (returncode, stdout).
        If the command sets an environment variable, it is appended to the environment list"""
        print("    >> {}     # (env variables: {})\n".format(cmd, environment))
        if cmd.strip().startswith("export"):
            environment += [cmd.replace("export","").strip()]
            return 0, ""
        else:
            result = self.container.exec_run(cmd, workdir=workdir, environment=environment)
            print(result.output.decode("utf8"))
            return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Delete container {}".format(self.name))
        self.container.stop()
        self.container.remove()

    def cp_out(self, path1, path2):
        raise NotImplementedError()

    def cp_in(self, path1, path2):
        with InParentDir(path1) as pardir:
            writetar = tf.open(name='/tmp/docoffe_tar.tar', mode='w|')
            writetar.add(os.path.relpath(path1, pardir.work_dir))
            writetar.close()
        with open('/tmp/docoffe_tar.tar', 'rb') as f:
            self.container.put_archive(path=path2, data=BytesIO(f.read()))


def run_one_container(program):
    check_docker()
    coffedir = autodetect_coffe()
    assert program in IMAGES
    yml_commands = extract_yml_cmds(coffedir, IMAGES[program])
    environment = []
    with InteractiveDockerContainer(program) as dk:
        # copy coffe directory into container
        dk.cp_in(coffedir, "/tmp")
        # own all files
        whoami = dk('whoami',
                    workdir="/tmp/coffe", environment=environment
                    ).output.decode("utf8").strip()
        dk("sudo chown -R {} .".format(whoami), workdir="/tmp/coffe", environment=environment)
        # remove cache files from coffe directory (piping does not work here)
        rm_files = dk('find . -name "*.pyc"',
                      workdir="/tmp/coffe", environment=environment
                      ).output.decode("utf8").split()
        rm_files += dk('find . -name "__pycache__"',
                       workdir="/tmp/coffe", environment=environment
                       ).output.decode("utf8").split()
        dk('rm -r {}'.format(" ".join(rm_files)), workdir="/tmp/coffe", environment=environment)
        # run commands
        exit_code = 0
        for cmd in yml_commands:
            exit_code, _ = dk(cmd, workdir="/tmp/coffe")
        return exit_code


class Rainbow:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    @classmethod
    def print(cls, msg, *args):
        res = msg
        for a in args:
            res = a + res + cls.END
        print(res)


@click.command()
@click.option("-p","--program", type=str,
              help="denotes the simulation program (and respective docker container)"
                   "that should be used for testing "
                   "and has to be one of the following: (no, amb, gmx, chm)."
                   "If the program is not specified, run all."
              )
def main(program):
    """
    Local docker runner for coffe's CI framework.
    """
    if program is not None:
        run_one_container(program)
    else:
        exit_codes = {k: None for k in IMAGES}
        for k in IMAGES:
            exit_codes[k] = run_one_container(k)

        Rainbow.print("----- SUMMARY -----", Rainbow.BOLD)
        for k in IMAGES:
            result = "OK" if exit_codes[k] == 0 else "ERROR"
            color = Rainbow.GREEN if exit_codes[k] == 0 else Rainbow.RED
            Rainbow.print(" {:<6} ... {:<6} ".format(k, result), Rainbow.BOLD, color)


if __name__ == "__main__":
    main()
