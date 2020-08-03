from numpy.distutils.core import setup
from setuptools import find_packages
import os

package_name = "simframe"

setup(
    name=package_name,
    use_scm_version=True,
    description="Framework for scientific simulations",
    long_description=open(os.path.join(
        os.path.dirname(__file__), "Readme.md")).read(),
    url='https://github.com/stammler/simframe',
    author="Sebastian Stammler & Til Birnstiel",
    author_email="stammler@usm.lmu.de; til.birnstiel@lmu.de",
    packages=find_packages(),
    license="GPLv3",
    install_requires=["numpy", "h5py", "pytest"],
    include_package_data=True,
    zip_safe=False,
    )