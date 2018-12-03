#!/usr/bin/env python

import io
import glob
import os

import setuptools


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ).read()


setuptools.setup(
    name="zotero2slack",
    version="0.2",
    license="GNU General Public License v3",
    description="A tail-f-like utility for JSON feeds",
    long_description=read("README.md"),
    author="James Webber",
    author_email="j@meswebber.com",
    url="https://github.com/jamestwebber/zotero2slack",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob.glob("src/*.py")
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=["click", "html2text", "PyYAML", "requests"],
    entry_points={"console_scripts": ["zotero2slack = zotero2slack:main"]},
)
