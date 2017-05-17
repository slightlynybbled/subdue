#!/usr/bin/env python

from setuptools import setup, find_packages


requirements = [
    "eventlet >= 0.21.0",
    "flask >= 0.12",
    "mkdocs >= 0.15.3",
    "numpy >= 1.11.2",
    "pyvisa >= 1.8",
    "pydaqmx >= 1.3.2",
    "pytest >= 3.0.2",
    "waitress >= 1.0.0"
]

with open('readme.md', 'r') as f:
    long_description = f.read()

setup(
    name='subdue',
    version='v0.1.6',
    description='Hardware manipulation for National Instruments, Agilent, etc.',
    long_description=long_description,
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/subdue',
    license='MIT',
    keywords='test labview visa instrument hardware',
    packages=find_packages(),
    entry_points={'console_scripts': [
      'subdue = subdue.__main__:main']
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)

