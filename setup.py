from setuptools import setup, find_packages
import sys, os

version = '0.6.8'
readme_fd = open('README.rst')
readme = readme_fd.read()
readme_fd.close()


setup(name='pyhistorian',
      version=version,
      description="pyhistorian is a BDD tool for writing specifications using Given-When-Then template",
      long_description=readme,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Topic :: Software Development :: Documentation',
          'Topic :: Software Development :: Testing',
      ],
      keywords='bdd dsl python',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='http://github.com/hugobr/pyhistorian',
      license='MIT License',
      packages=['pyhistorian', 'pyhistorian.specs', ],
      package_dir={'pyhistorian': 'src', 'pyhistorian.specs': 'specs'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['should-dsl',
                        'termcolor',],
      entry_points="",
      )
