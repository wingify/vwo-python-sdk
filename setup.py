import os

from setuptools import setup
from setuptools.command.develop import develop
from setuptools import find_packages

here = os.path.join(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as _file:
  REQUIREMENTS = _file.read().splitlines()

with open(os.path.join(here, 'README.md')) as _file:
  README = _file.read()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        import subprocess

        print('\nRUNNING POST INSTALL DEVELOP SCRIPT \n')

        subprocess.call("pre-commit install;", shell=True)
        subprocess.call("chmod +x post-install.sh; ./post-install.sh", shell=True)  # noqa:E501

        print('\nDONE: RUNNING POST INSTALL DEVELOP SCRIPT \n')

        develop.run(self)


setup(
    name='vwo-python-sdk',
    version='1.0.0',
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
    cmdclass={
        'develop': PostDevelopCommand
    },
    packages=find_packages(
        exclude=['tests']
    ),
    install_requires=REQUIREMENTS
)
