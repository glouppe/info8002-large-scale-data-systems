import os
import re
import sys

from setuptools import find_packages
from setuptools import setup

packages = find_packages()

# Module requirements.
_install_requires = [
    "numpy",
]

_parameters = {
    "install_requires": _install_requires,
    "license": "BSD",
    "name": "fbw",
    "packages": packages,
    "platform": "any",
    "url": "https://github.com/JoeriHermans/info8002-redundant-fly-by-wire/"
}

setup(**_parameters)
