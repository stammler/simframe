from setuptools import find_packages
from setuptools import setup
from numpy.distutils.core import setup
import os

package_name = "simframe"

setup(
    name=package_name,
    description="Framework for scientific simulations",
    url='https://github.com/stammler/simframe',
    author="Sebastian Stammler & Til Birnstiel",
    author_email="stammler@usm.lmu.de; til.birnstiel@lmu.de",
    packages=find_packages(),
    license="GPLv3",
    install_requires=["numpy", "glob", "h5py", "pytest", "setuptools_scm"],
    include_package_data=True,
    zip_safe=False,
    version="0.1.0"
    )