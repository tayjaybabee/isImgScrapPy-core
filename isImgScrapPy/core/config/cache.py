"""

File: isImgScrapPy/core/config/cache.py
Project: isImgScrapPy-core
Description: 

Created: 10/20/22 - 20:01:06

"""
# Standard library imports
from time import time

# Non-Standard library imports
from appdirs import user_cache_dir
from configobj import ConfigObj
from pathlib import Path

# Project based imports
from isImgScrapPy.core.__about__ import \
    __prog__ as PROG, \
    __author__ as AUTHOR, \
    __version__ as VERSION


CACHE_FILENAME = 'cache.conf'
CACHE_DIR = Path(user_cache_dir(appname=PROG, appauthor=AUTHOR, version=VERSION))
CACHE_FP = CACHE_DIR.joinpath(CACHE_FILENAME)


class Cache(ConfigObj):
    def __init__(self, write_on_change=False):
        """
        Instantiate the cache.

        Arguments:
          write_on_change (bool):
              Whether to write the cache to storage when its contents are changed. (Optional; defaults to :bool:`False`)
        """
        self.__filepath = str(CACHE_FP)
        super(Cache, self).__init__(self.__filepath)

        self.__write_on_change = write_on_change

        self.fields = [
                'config_filepath',
                'config_pathlock',
        ]
        self['config_filepath'] = None
        self['config_pathlock'] = False

        if not Path(self.__filepath).parent.exists():
            Path(self.__filepath).parent.mkdir(parents=True)

        if not Path(self.__filepath).exists():
            self.create()
        else:

    @property
    def write_on_change(self):
        return self.__write_on_change

    @write_on_change.setter
    def write_on_change(self, new: bool):
        if isinstance(new, bool):
            self.__write_on_change = new

    @property
    def filepath(self):
        return self.__filepath

    @property
    def first_run(self):
        return self['runs']['first']

    @property
    def last_run(self):
        return self['runs']['last']

    @property
    def config_filepath(self):
        return self['config']['filepath']

    @config_filepath.setter
    def config_filepath(self, new):
        if self.config_filepath is None:
            new = Path(new).expanduser().resolve()

    @property
    def runs(self):
        return self['runs']

    def save(self):
        with open(self.__filepath, 'w') as file:
            self.write(file)

    def create(self):
        self.merge(self.get_new())

    @property
    def last_run(self):
        return self['last_run']

    @staticmethod
    def get_new():
        return {
                'runs': {
                        'first': {
                                'timestamp': time(),
                                'version': VERSION
                        },
                        'last': {
                                'timestamp': time(),
                                'version': VERSION,
                        },
                        'num': 1
                        }
                }



    @property
    def age(self):
        m2 = time()
        return m2 - self['first_run']
