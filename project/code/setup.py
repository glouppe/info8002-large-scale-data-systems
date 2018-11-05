"""
KeyChain setup file (stub).

NB: Feel free to extend or modify.
"""

import os
import re

from setuptools import find_packages
from setuptools import setup


exclusions = ["doc", "experiments", "application"]
packages = find_packages(exclude=exclusions)

# Get the version string of cag.
with open(os.path.join("keychain", "__init__.py"), "rt") as fh:
    _version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        fh.read()
    ).group("version")

# Module requirements.
_install_requires = [
    "argparse",
    "flask",
    "hashlib",
    "numpy",
    "requists",
    "time"
]

_parameters = {
    "install_requires": _install_requires,
    "license": "BSD",
    "name": "cag",
    "packages": packages,
    "platform": "any",
    "url": "https://github.com/glouppe/info8002-large-scale-data-systems",
    "version": _version
}

setup(**_parameters)
