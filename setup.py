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
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="numerical,simulation,integration,science,mathematics,physics",

    url="https://github.com/stammler/simframe",
    project_urls={"Source Code": "https://github.com/stammler/simframe/",
                  "Documentation": "https://simframe.readthedocs.io/"
                  },

    author="Sebastian Stammler, Til Birnstiel",
    author_email="sebastian.stammler@gmail.com, til.birnstiel@lmu.de",
    maintainer="Sebastian Stammler",

    version=read_version(),
    license="GPLv3",

    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3 :: Only",
                 "Topic :: Education",
                 "Topic :: Scientific/Engineering",
                 "Topic :: Scientific/Engineering :: Mathematics",
                 "Topic :: Scientific/Engineering :: Physics",
                 ],

    packages=find_packages(),
    install_requires=["dill", "h5py", "numpy", "pytest", "scipy"],
    include_package_data=True,
    zip_safe=False,
)
