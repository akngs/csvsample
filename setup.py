from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='csvsample',
    version='0.1.4',
    description='Create random samples from CSV file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/akngs/csvsample',
    author='Alan Kang',
    author_email='jania902@gmail.com',

    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',

        'License :: OSI Approved :: MIT License',

        'Topic :: Text Editors :: Text Processing',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['fire', 'xxhash'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest'],
    },

    entry_points={
        'console_scripts': [
            'csvsample=csvsample:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/akngs/csvsample/issues',
        'Source': 'https://github.com/akngs/csvsample/',
    },
)
