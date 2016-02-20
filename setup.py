import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
        README = f.read()

exec(open(os.path.join(here, 'jenkins_cli/version.py')).read())

requires = [ 'pbr>=1.3.0',
             'python-jenkins>=0.4.8',
             'six>=1.9.0' ]

setup(
    name='jenkins-cli',
    version=version,
    description='Commandline interface for Jenkins',
    long_description=README,
    author='Denys Levchenko',
    keywords='jenkins, commandline, cli',
    license='http://opensource.org/licenses/MIT',
    packages=find_packages(),
    install_requires=requires,
    entry_points = {
      'console_scripts' : [ 'jenkins = jenkins_cli:main' ]
    }
)
