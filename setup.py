from setuptools import find_packages
from setuptools import setup
import pathlib

package_name = "simframe"
here = pathlib.Path(__file__).absolute().parent


def read_version():
    with (here / package_name / '__init__.py').open() as fid:
        for line in fid:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


setup(
    name=package_name,
    description="Framework for scientific simulations",
    summary="Framework for scientific simulations",
    keywords="numerical,simulation,integration",
    home_page="https://github.com/stammler/simframe",
    url="https://github.com/stammler/simframe",
    author="Sebastian Stammler, Til Birnstiel",
    author_email="stammler@usm.lmu.de, til.birnstiel@lmu.de",
    packages=find_packages(),
    license="GPLv3",
    install_requires=["dill", "h5py", "numpy", "pytest", "scipy"],
    include_package_data=True,
    zip_safe=False,
    version=read_version(),
)
