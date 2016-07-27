import re
import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

def read(*parts):
    return open(os.path.join(os.path.dirname(__file__), *parts)).read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")



setup(
    name='django-single-email-confirmation',
    version=find_version('single_email_confirmation', '__init__.py'),
    author='Emīls kalniņš',
    author_email='emils.kalnins@outlook.com',
    description="Email confirmation for django models.",
    long_description=read('README.rst'),
    url='https://github.com/mfogel/django-simple-email-confirmation',
    license='The Unlicense',
    packages=find_packages(),
    install_requires=['django>=1.9.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        'License :: The Unlicense',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        "Framework :: Django",
    ]
)
