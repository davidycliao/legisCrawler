# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand
import re

for line in open('legislators/__init__.py'):
    match = re.match("__version__ *= *'(.*)'", line)
    if match:
        __version__, = match.groups()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        raise SystemExit(errno)


setup(name='legisCrawler',
      version=__version__,
      description='An Automation Webcrawling Toolkit for Taiwan Parliamentary Questions',
      maintainer='David, Yen-Chieh Liao',
      maintainer_email='davidycliao@gmail.com',
      url='https://github.com/davidycliao/legisCrawler',
      packages=['legisCrawler'],
      keywords=['legislative-yuan', 'parliamentary-questions', 'selenium'],
      install_requires=[
          'numpy>1.16.2',
          'scipy>=1.5.1',
          'pandas',
          'matplotlib',
          'selenium',
          'webdriver_manager'
      ],
      tests_require=['pytest', 'mock'],
      cmdclass={'test': PyTest},
      license='MIT License'
)
