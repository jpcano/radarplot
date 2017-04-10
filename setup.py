"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='radarplot',
    version='1.0.0',
    description='Library to read and plot radar images specified by CIKM AnalytiCup 2017',
    long_description=long_description,
    url='https://github.com/jpcano/radarplot',
    author='Jesus Cano',
    author_email='me@jesus.engineer',
    license='GNU GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],
    
    keywords='machine learning, image radar, methereology, deeplearning',
    packages=find_packages(exclude=['tests']),
    package_data={'data': ['data_sample.txt'],
},
    install_requires=['matplotlib'],
)
