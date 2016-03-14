from setuptools import setup, find_packages
import os

from babel.messages.frontend import compile_catalog, extract_messages, init_catalog, update_catalog

from distutils.command.build import build as _build

import ipodshuffle.version


__version__ = ipodshuffle.version.__version__

NAME = "ipodshuffle"

VERSION = __version__

DESCRIPTION = 'modules and tools for iPod shuffle 4th generation'

LONG_DESCRIPTION = ''
if os.path.exists('long_description.rst'):
    LONG_DESCRIPTION = open('long_description.rst').read()
elif os.path.exists('README.rst'):
    LONG_DESCRIPTION = ''.join(open('README.rst').readlines()[3:9])

URL = 'https://github.com/meng89/{}'.format(NAME)

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


class Build(_build):
    sub_commands = [('compile_catalog', None)] + _build.sub_commands


def get_local_data_files():
    locale_files = []

    dirname = os.path.join(os.path.dirname(__file__), 'teresa')
    for lang_code in os.listdir(os.path.join(dirname, 'locale')):

        locale_files.append(
            ('share/locale/'+lang_code+'/LC_MESSAGES', [dirname + '/locale/'+lang_code+'/LC_MESSAGES/teresa.mo'])
        )

    return locale_files

DATA_FILES = get_local_data_files()


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
      message_extractors={
          'ipodshuffle/tools': [
              ('**.py', 'python', None),
          ]
      },
      install_requires=[
          'langid>=1.1.5',
          'mutagen>=1.27',
          'Babel'
      ],
      entry_points={
          'console_scripts': [
              'teresa=teresa.__main__:main',
          ],
      },

      cmdclass={
          'compile_catalog': compile_catalog,
          'extract_messages': extract_messages,
          'init_catalog': init_catalog,
          'update_catalog': update_catalog,

          'build': Build
      },
      data_files=DATA_FILES
      )
