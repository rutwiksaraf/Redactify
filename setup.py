from setuptools import setup, find_packages
from setuptools.command.install import install
import os

# Custom command to download the 'en_core_web_lg' model after installation
class CustomInstall(install):
    def run(self):
        install.run(self)  # Install all dependencies
        os.system('python -m spacy download en_core_web_lg')  # Download the Spacy model

setup(
    name='project1',
    version='1.0',
    author='Your Name',
    author_email='your ufl email',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'spacy'],
    install_requires=[
        'spacy'
    ],
    cmdclass={
        'install': CustomInstall,  # Add the custom install command
    }
)
