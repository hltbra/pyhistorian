from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='pyhistorian',
      version=version,
      description="pyhistorian is a tool for writing specifications using Given-When-Then template",
      long_description="",
      classifiers=[],
      keywords='bdd dsl python',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='http://code.google.com/p/pyhistorian/',
      license='MIT License',
      packages=['pyhistorian'],
      package_dir={'pyhistorian': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools'],
      entry_points="",
      )
