"""A simple setup module for MkDocs-Merge, based on the pip setup.py file.
See:
https://github.com/pypa/pip/blob/1.5.6/setup.py
"""

import codecs
import os
import re
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Package description
setup(
    name='mkdocs-merge',
    version=find_version('mkdocsmerge', '__init__.py'),
    description='Simple to merge multiple MkDocs sites into a single directory',
    url='https://github.com/ovasquez/mkdocs-merge.git',
    license='MIT',
    author='Oscar Vasquez',
    author_email='',
    keywords=['mkdocs', 'documentation', 'merge', 'multiple'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=5.0',
        'mkdocs>=0.16',
        'ruamel.yaml>=0.15'
    ],
    entry_points={
        "console_scripts": [
            "mkdocs-merge = mkdocsmerge.__main__:cli"
        ]
    },
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False
)
