"""

File: isImgScrapPy/core/config/__init__.py
Project: isImgScrapPy-core
Description: 

Created: 10/18/22 - 12:13:42

"""
from appdirs import user_cache_dir, user_data_dir, user_config_dir
from configobj import ConfigObj
from time import time

from pathlib import Path
from os import makedirs
from shutil import copy

from isImgScrapPy.core.__about__ import __prog__ as PROG, __author__ as AUTHOR, __version__ as VERSION
from isImgScrapPy.core.config.cache import Cache

CONFIG_FILENAME = 'config.ini'
DEFAULT_CONFIG_DIR = Path(user_config_dir(appname=PROG, appauthor=AUTHOR)).joinpath('config')
DEFAULT_CONFIG_FP = DEFAULT_CONFIG_DIR.joinpath(CONFIG_FILENAME)


def check_config_file(config_fp=None, no_cache=False):
    if not no_cache:
        cache = Cache()

CACHE = Cache()


class Config(ConfigObj):
    def __init__(
            self,
            config_fp=None,
            auto_replace_config:bool=False,
            no_backups:bool=False,

    ):
        if config_fp is None and 'config_directory' not in CACHE.keys():
            config_fp = DEFAULT_CONFIG_FP
            CACHE['config_directory'] = config_fp.parent
            CACHE.write()

        if config_fp is not None and 'config_directory' in CACHE.keys():
            if auto_replace_config:
                if not no_backups:
                    copy(Path(CACHE['config_directory']).joinpath(), )





        elif len(CACHE.items()) >= 1:
            config_fp
            config_fp = Path(config_fp).expanduser().resolve()

        super(Config, self).__init__(config_fp)
