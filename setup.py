import murloc
from setuptools import setup, find_packages

setup(
    name="murloc",
    version="1.0.0",
    author="Chris Varga",
    author_email="",
    description="Extensible API server",
    long_description=help(murloc),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="extensible api server",
)
