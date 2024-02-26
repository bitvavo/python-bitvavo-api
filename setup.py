from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="python_bitvavo_api",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="1.4.1",
    author="Bitvavo",
    description="Use Bitvavo SDK for Python to buy, sell, and store over 200 digital assets on Bitvavo from inside your app.",
    url="https://github.com/bitvavo/python-bitvavo-api",
    packages=find_packages(),
    install_requires=[
        'websocket-client',
        'requests==2.31.0',
        'setuptools'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
