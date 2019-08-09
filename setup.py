import os

from setuptools import setup, find_packages
from setuptools.command.develop import develop

current_directory = os.path.join(os.path.dirname(__file__))

with open(os.path.join(current_directory, 'requirements.txt')) as f:
  REQUIREMENTS = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        import subprocess

        print('\nRUNNING POST INSTALL DEVELOP SCRIPT \n')

        subprocess.call("pre-commit install;", shell=True)  # skipcq: BAN-B602
        # skipcq: BAN-B602
        subprocess.call("chmod +x post-install.sh; ./post-install.sh", shell=True)  # noqa:E501

        print('\nDONE: RUNNING POST INSTALL DEVELOP SCRIPT \n')

        develop.run(self)


setup(
    name='vwo-python-sdk',
    version='1.0.2',
    description='Python SDK for VWO server-side A/B Testing',
    long_description='Some issue with twine rendering markdown README.md',
    author='VWO',
    author_email='dev@wingify.com',
    url='https://github.com/wingify/vwo-python-sdk',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    cmdclass={
        'develop': PostDevelopCommand
    },
    packages=find_packages(
        exclude=['tests']
    ),
    install_requires=REQUIREMENTS
)
