import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
        README = f.read()

exec(open(os.path.join(here, 'jenkins_cli/version.py')).read())

requires = ['pbr>=1.3.0',
            'python-jenkins>=0.4.8',
            'six>=1.9.0']

test_require = ['unittest2',
                'mock']

setup(
    name='jenkins-cli',
    version=version,
    description='Commandline interface for Jenkins',
    long_description=README,
    author='Denys Levchenko',
    keywords='jenkins, commandline, cli',
    license='http://opensource.org/licenses/MIT',
    classifiers=(
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 2',
      'License :: OSI Approved :: MIT License',
    ),
    packages=find_packages(),
    install_requires=requires,
    test_require=test_require,
    test_suite="tests",
    entry_points={
      'console_scripts': ['jenkins = jenkins_cli:main']
    }
)
