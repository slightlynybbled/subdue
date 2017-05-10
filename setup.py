#!/usr/bin/env python

from setuptools import setup, find_packages
from subdue import __version__

requirements = [
    "flask >= 0.12",
    "gevent >= 1.2",
    "mkdocs >= 0.15.3",
    "numpy >= 1.11.2",
    "pyvisa >= 1.8",
    "pydaqmx >= 1.3.2",
    "pytest >= 3.0.2",
]

setup(name='subdue',
      version=__version__,
      description='Hardware manipulation for National Instruments, Agilent, etc.',
      author='Jason R. Jones',
      author_email='slightlynybbled@gmail.com',
      url='https://bitbucket.org/jjonesAtMoog/ams_hw_suite',
      packages=find_packages(),
      entry_points={'console_scripts': [
          'ams_hw_suite = ams_hw_suite.__main__:main']
      },
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False
      )

