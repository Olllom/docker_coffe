# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
    'Click>=6.0',
    'six',
    'docker'
]


setup(
    name='coffe_docker',
    version='0.1.0',
    description="Dockerfiles for Comprehensive Optimization Force Field Environment",
    author="Andreas Krämer",
    author_email='kraemer.research@gmail.com',
    url='https://github.com/Olllom/docker_coffe',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docoffe=docoffe:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='coffe',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
