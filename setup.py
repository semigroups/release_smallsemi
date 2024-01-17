"""
A script for releasing the Smallsemi GAP package.
"""
import os

from setuptools import find_packages, setup


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + "/requirements.txt"
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath, "r", encoding="utf8") as f:
        install_requires = f.read().splitlines()

setup(
    name="release_smallsemi",
    version="0.0.0",
    py_modules=["release_smallsemi"],
    url="",
    license="GPL3",
    author="James D. Mitchell",
    author_email="jdm3@st-andrews.ac.uk",
    description=("A script for releasing the SmallSemi GAP package."),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["release_smallsemi = release_smallsemi:main"]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
