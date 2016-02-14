from setuptools import setup, find_packages
import os

NAME = "ipodshuffle"

VERSION = '0.2.4'

DESCRIPTION = 'A Python library and CLI tools for iPod shuffle 4th generation with VoiceOver(TTS) support'

LONG_DESCRIPTION = ''
if os.path.exists('long_description.rst'):
    LONG_DESCRIPTION = open('long_description.rst').read()


URL = 'https://github.com/meng89/{}'.format(NAME)

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='MIT',
      url=URL,
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      install_requires=[
          'langid>=1.1.5',
          'mutagen>=1.27'
      ],
      entry_points={
          'console_scripts': [
              'teresa=ipodshuffle.tools.teresa:main',
          ],
      },
      )
