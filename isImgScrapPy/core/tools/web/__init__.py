""" A module containing functions that pertain to interfacing with the web. """
from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
from isImgScrapPy.core.tools.web.errors import URLValidationError, RemoteFileNotFoundError, AttributeNotSetError
from isImgScrapPy.core.tools.progress import PROGRESS
from isImgScrapPy.core.images import DEFAULT_IMG_DEST as DEFAULT_DEST
from pathlib import Path
from urllib import request as ulreq
from PIL import ImageFile
from tqdm import tqdm, trange

from concurrent.futures import ThreadPoolExecutor


from os import makedirs
import shutil

try:
    # python 3
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def get_remote_image_size(uri):
    """
    The get_sizes function accepts a URL as an argument and returns the size of the image at that URL. It does this by
    using urllib to open up the file, then it gets its content length (if available) and feeds that data into an
    ImageFile parser. If there is no content length, it will return None

    Arguments:
        uri (string):
            Specify the location of the image

    Returns:
        The size of the image file and the size of the image itself
    """
    # get file size *and* image size (None if not known)
    file = ulreq.urlopen(uri)
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
        break
    file.close()
    return size, None


def validate_url(url):
    """
    The validate_url function checks if the url is valid.
    It checks if the scheme, netloc and path are present in the URL.

    Args:
        url: Specify the url to validate

    Returns:
        True if the url is valid and false otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except Exception:
        return False


def get_4chan_board_and_thread(url):
    url_parts = url.split('/')
    print(url_parts)
    return {
            'board':  url_parts[3],
            'thread': url_parts[5]
    }


class ImageUrl(object):
    def __init__(self, url, dest=None, chan=False, board=None, thread=None):
        """
        The __init__ function is called when an instance of the class is created.
        It initializes all of the attributes that are defined in the class.


        Args:
            self: Refer to the object itself
            url: Set the url of the image to be downloaded
            dest=None: Set the default value for dest
            chan=False: Specify whether the image is from 4chan or a chan link
            board=None: Set the board value for a chan link
            thread=None: Set the chan_link attribute to true

        Instance Methods --------------------------------

            - ImageUrl:
                - .download
                - .gather_info
                - .validate


        Attributes:
            ImageUrl.name (str):
                The name of the image, not including the extension or path. (str)

            ImageUrl.URL (str):
                The URL string of the image.

            ImageUrl.full_name (str):
                The full name of the image file, including the extension, but not the path.

            ImageUrl.extension (str):
                The extension of the image file. (I.E; 'jpg', 'jpeg', 'png', etc)

                Note:
                    The following alias(es) are supported for :attr:`ImageUrl.extension`:

                        - `ImageUrl.ext`

            ImageUrl.px_size (tuple(int, int):
                The size of the image in pixels. (I.E; `tuple(1920,1080)`

                Note:
                    The following alias(es) are supported for :attr:`ImageUrl.px_size`:

                        - `ImageUrl.pixel_size`


        """

        self.__chan_link = chan
        self.__chan_board = None
        self.__chan_thread = None

        url_obj = url

        if chan:

            try:
                url = url_obj['href']
            except KeyError:
                url = None

            if thread is None or board is None:
                raise ValueError("Setting 'chan' to True and not providing values for `board` and `thread` is not \""
                                 "supported behavior.")
            self.__chan_board = board
            self.__chan_thread = thread


        else:
            url = url_obj['src']

        if url.startswith('//'):
            url = f'https:{url}'

        if validate_url(url):
            self.__url = url
        else:
            raise URLValidationError(url = url)

        self.__img_local_filepath = None

        self.__dest_dir = DEFAULT_DEST if dest is None else Path(dest)

        if self.__dest_dir == DEFAULT_DEST and chan:
            self.__dest_dir = Path(self.__dest_dir).joinpath(f'{board}/{thread}')

        self.__url_parts = None
        self.__img_data_size = None
        self.__img_px_size = None
        self.__img_name = None
        self.__img_full_name = None
        self.__img_ext = None
        self.__img_status_code = None

        self.gather_info()

    def gather_info(self):

        url = self.URL

        if 'i.4cdn.org' in self.URL and self.URL.endswith(f's.{self.URL[-3:]}'):
            self.__chan_link = True
            url = self.URL.replace(f's.{self.URL[-3]}', f'.{self.URL[-3]}')
            self.__dest_dir = self.__dest_dir.joinpath(f'4chan/{self.__chan_board}/{self.__chan_thread}')

        name = ''.join(url.split('/')[-1].split('.')[:-1])
        extension = url.split('/')[-1].split('.')[-1]
        disk_size, px_size = get_remote_image_size(url)

        self.__img_name = name
        self.__img_ext = extension
        self.__img_full_name = f'{name}.{extension}'
        self.__img_data_size = disk_size
        self.__img_px_size = px_size

        self.__img_local_filepath = self.__dest_dir.joinpath(self.__img_full_name)

    @property
    def local_filepath(self):
        return self.__img_local_filepath

    def download(self, dest=None, name=None, ext=None):
        dest = self.__img_local_filepath if dest is None else Path(dest)

        # The name of our file without the extension
        f_name = self.name

        res = requests.get(self.URL, stream = True)

        if not self.destination_directory.exists():
            makedirs(self.destination_directory)

        if res.status_code == 200:
            res.raw.decode_content = True
            with tqdm.wrapattr(open(dest, 'wb'), "write",
                               miniters=1,
                               desc=self.URL.split('/')[-1],
                               total=int(res.headers.get('content-length', 0)),
                               leave=False

                               ) as fout:
                for chunk in res.iter_content(chunk_size=4096):
                    fout.write(chunk)
#            with open(self.destination_directory.joinpath(self.full_name), 'wb') as fd:
#                shutil.copyfileobj(res.raw, fd)

    def validate(self, url=None):
        return validate_url(url or self.URL)

    @property
    def URL(self):
        """ Return the URL for this image file. """
        return self.__url

    @property
    def disk_size(self):
        """ Return the disk size of this image file. """
        if self.__img_data_size is None:
            self.gather_info()
        return self.__img_data_size

    @property
    def px_size(self):
        """ Return the size of the image in pixels. """
        if self.__img_px_size is None:
            self.gather_info()
        return self.__img_px_size

    pixel_size = property(lambda self: self.px_size)
    """ An alias for the px_size property"""

    px_width = property(lambda self: self.pixel_size[0])
    """ An alias for the width part of the px_size property """

    px_height = property(lambda self: self.pixel_size[1])
    """ An alias for the pixel height."""

    @property
    def extension(self):
        """ Return the file extension. """
        if self.__img_ext is None:
            self.gather_info()
        return self.__img_ext

    ext = property(lambda self: self.extension)
    """ An alias for the `extension` property. """

    @property
    def name(self):
        """ Return the file name for this image file sans the extension or path."""
        if self.__img_name is None:
            self.gather_info()
        return self.__img_name

    @property
    def full_name(self):
        """ Return the full name of the file including the extension. """
        if self.__img_full_name is None:
            self.gather_info()
        return self.__img_full_name

    @property
    def destination_directory(self):
        """ Return the destination directory for this file when downloaded. """
        if self.__dest_dir is None:
            self.gather_info()
        return self.__dest_dir

    dest_dir = property(lambda self: self.destination_directory)
    """ An alias for the destination directory property"""

    @property
    def full_filepath(self):
        """ Return the destination for this file when downloaded. """
        if self.__img_local_filepath is None:
            self.gather_info()
        return self.__img_local_filepath

    @property
    def all_info(self):
        """ Return a list of all information about this image. """

        return {
                'URL':                   self.URL,
                'px_size':               self.px_size,
                'disk_size':             self.disk_size,
                'extension':             self.extension,
                'name':                  self.name,
                'full_name':             self.full_name,
                'destination_directory': self.destination_directory,
                'local_filepath':        self.full_filepath,

        }

    def __repr__(self):
        attribute_substr = '\n' \
                           'Attributes:\n'
        for key, value in self.all_info.items():
            key = key.replace('_', ' ').title()
            attribute_substr += f'  | {key}:\n    {value}\n'

        return f"<ImageURL: {self.URL}>{attribute_substr}"

    def __dict__(self):
        return dict(self.all_info)

    def __all__(self):
        return self.all_info


class PageInfo(object):
    def __init__(self, url, auto_gather_images=False):

        if not validate_url(url):
            raise URLValidationError
        self.__auto_gather = auto_gather_images
        self.__url = url

        self.__img_links = []
        self.__results = None
        self.__res_status_code = None
        self.__soup = None
        self.__src_counters = 0
        self.__chan_link = False
        self.__chan_board = None
        self.__chan_thread = None

        if self.__auto_gather:
            self.gather_image_links()


    @property
    def auto_gather_images(self):
        return self.__auto_gather

    @property
    def results(self):
        if not self.__results:
            try:
                self.__results = requests.get(self.URL)
                self.__res_status_code = self.__results.status_code
                if self.__res_status_code != 200 and self.__results.status_code == 404:
                    raise RemoteFileNotFoundError(self.URL)
            except HTTPError as e:
                print(e)
        return self.__results

    @property
    def result_data(self):
        if not self.__results:
            self.__results = self.results
        return self.__results.text

    @property
    def soup(self):
        return BeautifulSoup(self.result_data, 'html.parser')

    @property
    def URL(self):
        return self.__url

    @property
    def image_links(self):
        return self.__img_links

    @property
    def chan_board(self):
        if not self.__chan_link:
            raise AttributeNotSetError(attribute_name = 'chan_board')
        return self.__chan_board

    @property
    def chan_thread(self):
        if not self.__chan_link:
            raise AttributeNotSetError(attribute_name = 'chan_thread')
        else:
            return self.__chan_thread

    def add_link(self, link):
        print(link)

        if self.__chan_link and self.__chan_board is None:
            bt = get_4chan_board_and_thread(url = self.URL)
            self.__chan_board = bt['board']
            self.__chan_thread = bt['thread']

        link = ImageUrl(link, chan = self.__chan_link, board = self.__chan_board, thread = self.__chan_thread)

        self.__img_links.append(link)
        self.__src_counters += 1

    def from_4chan_url(self):

        url = self.URL
        soup = self.soup
        self.__chan_link = True

        for item in soup.find_all('a', { 'class': 'fileThumb' }):
            self.add_link(item)

    def gather_image_links(self):
        if len(self.__img_links) != 0:
            return self.__img_links

        url = self.URL
        if '4chan' in url:
            self.from_4chan_url()
            # for item in soup.find_all('a', {'class': 'fileThumb'}):
            #     self.image_info = item
            #     self.__src_counters[url] += 1
            #     print(self.__src_counters[url])
            #     out_dev(item)

        else:

            soup = self.soup
            for item in soup.find_all('img'):
                if 'nsfwupload.com/content/' not in item['src']:
                    self.image_info = item
                    out_dev(item)

        return self.__img_links

    def download_all(self):
        for img in tqdm(self.image_links, desc=f'Downloading all images from {self.chan_board}/{self.chan_thread}'):
            img.download()





    def __repr__(self):
        return f'<PageInfo: {self.URL}>'
