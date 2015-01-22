from setuptools import setup
import os
try:
    import pypandoc
    description=pypandoc.convert('readme.md','rst')
except:
    description=''
setup(name='fbadmin',
      version='0.1.0.2',
      description='A python library to automate facebook group administration',
      long_description=description,
      url='https://github.com/thekindlyone/fbadmin',
      author='thekindlyone',
      author_email='dodo.dodder@gmail.com',
      license='GNU GPL v2',
      packages=['fbadmin'],
      install_requires=[
          'selenium',
             ],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7"          
      ],
      zip_safe=False)