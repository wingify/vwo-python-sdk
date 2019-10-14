import os

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools import Command

import subprocess

current_directory = os.path.join(os.path.dirname(__file__))

with open(os.path.join(current_directory, 'requirements.txt')) as f:
  REQUIREMENTS = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()


class ReleasePatchCommand(Command):
    description = "Patch Release"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call("bumpversion patch", shell=True)


class ReleaseMinorCommand(Command):
    description = "Minor Release"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call("bumpversion minor", shell=True)


class ReleaseMajorCommand(Command):
    description = "Major Release"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call("bumpversion major", shell=True)


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        print('\nRUNNING POST INSTALL DEVELOP SCRIPT \n')

        subprocess.call("pre-commit install;", shell=True)  # skipcq: BAN-B602
        # skipcq: BAN-B602
        subprocess.call("chmod +x post-install.sh; ./post-install.sh", shell=True)

        print('\nDONE: RUNNING POST INSTALL DEVELOP SCRIPT \n')

        develop.run(self)


setup(
    name='vwo-python-sdk',
    version='1.1.1',
    description='Python SDK for VWO server-side A/B Testing',
    long_description='Some issue with twine rendering markdown README.md',
    author='VWO',
    author_email='dev@wingify.com',
    url='https://github.com/wingify/vwo-python-sdk',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'patch': ReleasePatchCommand,
        'minor': ReleaseMinorCommand,
        'major': ReleaseMajorCommand
    },
    packages=find_packages(
        exclude=['tests']
    ),
    install_requires=REQUIREMENTS
)
