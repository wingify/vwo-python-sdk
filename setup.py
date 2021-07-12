# Copyright 2019-2021 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# flake8: noqa

import os

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools import Command

import subprocess

current_directory = os.path.join(os.path.dirname(__file__))

with open(os.path.join(current_directory, "requirements.txt")) as f:
    REQUIREMENTS = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()


class DocCheckCommand(Command):
    description = "Doc Check"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call("python3 ./scripts/doc_check.py", shell=True)


class LicenseCheckCommand(Command):
    description = "License Check"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call(
            'python3 ./scripts/apache_license_check.py vwo/ tests/ setup.py --copyright "2019-2021 Wingify Software Pvt. Ltd."',
            shell=True,
        )


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
        print("\nRUNNING POST INSTALL DEVELOP SCRIPT \n")

        subprocess.call("pre-commit install;", shell=True)  # skipcq: BAN-B602
        # skipcq: BAN-B602
        subprocess.call("chmod +x post-install.sh; ./post-install.sh", shell=True)

        print("\nDONE: RUNNING POST INSTALL DEVELOP SCRIPT \n")

        develop.run(self)


setup(
    name="vwo-python-sdk",
    version="1.18.0",
    description="Python SDK for VWO server-side A/B Testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="VWO",
    author_email="dev@wingify.com",
    url="https://github.com/wingify/vwo-python-sdk",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={
        "develop": PostDevelopCommand,
        "patch": ReleasePatchCommand,
        "minor": ReleaseMinorCommand,
        "major": ReleaseMajorCommand,
        "license_check": LicenseCheckCommand,
        "doc_check": DocCheckCommand,
    },
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
)
