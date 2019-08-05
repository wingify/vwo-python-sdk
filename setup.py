import os

from setuptools import setup
from setuptools import find_packages

here = os.path.join(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as _file:
  REQUIREMENTS = _file.read().splitlines()

with open(os.path.join(here, 'README.md')) as _file:
  README = _file.read()

setup(
    name='vwo-python-sdk',
    version='0.1.0-alpha.10',
    description='Python SDK for VWO server-side A/B Testing',
    long_description=README,
    long_description_content_type='text/markdown',
    author='VWO',
    author_email='dev@wingify.com',
    url='https://github.com/wingify/vwo-python-sdk',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(
        exclude=['tests']
    ),
    install_requires=REQUIREMENTS
)
