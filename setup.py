import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()

version_file_content = open(os.path.join(here, 'jenkins_cli/version.py')).read()
version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]",
                          version_file_content, re.M)
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError('Unable to find version string.')

requires = ['python-jenkins==0.4.14',
            'six>=1.9.0',
            'pyxdg>=0.25']

tests_require = ['unittest2==1.1.0',
                 'mock==2.0.0',
                 'pyfakefs==2.7.0']

data_files = []
completion_dirs = ['/usr/share/bash-completion/completions',
                   '/usr/local/opt/bash-completion/etc/bash_completion.d']

if os.geteuid() == 0:
    for d in completion_dirs:
        if os.path.isdir(d):
            data_files.append((d, ['contrib/bash-completion/jenkins']))
else:
    print("Non-root user detected. Bash completion won't be installed.")

setup(
    name='jenkins-cli',
    version=version,
    description='Commandline interface for Jenkins',
    long_description=README,
    author='Denys Levchenko',
    author_email='denis.levtchenko@gmail.com',
    url='https://github.com/LD250/jenkins-cli-python',
    keywords='jenkins, commandline, cli',
    license='http://opensource.org/licenses/MIT',
    classifiers=(
      'Natural Language :: English',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'License :: OSI Approved :: MIT License',
    ),
    packages=find_packages(),
    install_requires=requires,
    tests_require=tests_require,
    test_suite="tests",
    data_files=data_files,
    entry_points={
      'console_scripts': ['jenkins = jenkins_cli:main']
    }
)
