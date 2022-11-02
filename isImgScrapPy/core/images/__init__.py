from appdirs import user_data_dir
from isImgScrapPy.core.__about__ import __prog__ as PROG, __author__ as AUTHOR
from isImgScrapPy.core.tools.web.errors import URLValidationError

from urllib import request as ulreq
import requests
import shutil

from pathlib import Path
from PIL import ImageFile
from PIL import BmpImagePlugin as Bmp, \
    JpegImagePlugin as Jpeg, \
    GifImagePlugin as Gif, \
    PngImagePlugin as Png, \
    TiffImagePlugin as Tiff


valid_types = (
    Bmp.BmpImageFile,
    Gif.GifImageFile,
    Jpeg.JpegImageFile,
    Png.PngImageFile,
    Tiff.TiffImageFile
)
""" The types of image-file objects accepted by the program. """

valid_extensions = [
    'bmp',
    'gif',
    'jpeg',
    'png',
    'tiff'
]
""" 
Mostly for helping the end-user, used to notify the user of what types of file objects are accepted if passed an 
invalid type 
"""


DEFAULT_IMG_DEST = Path(user_data_dir(appname=PROG, appauthor=AUTHOR)).joinpath('images')


def parse_remote_image_file(self, url):
    return



def valid_image_type(img_obj):
    """
    The valid_image_type function checks to see if the image object is an instance of one of the valid types.
    If it is, then it returns True. If not, a TypeError exception is raised.

    Args:
        img_obj (PIL.Image):
            Check if the image object is a valid image type

    Returns:
        The result of the isinstance function
    """
    if res := isinstance(img_obj, valid_types):
        return res
    else:
        raise TypeError(f'Image must be one of: {", ".join(valid_extensions)}')


def download_image(url, dest_fp):
    """
    The download_image function downloads an image from a given URL and saves it to the specified filepath.

    Args:
        url: Specify the url of the image that is to be downloaded
        dest_fp: Specify the file path where the image will be saved

    Returns:
        The name of the file that was downloaded
    """
    f_name = url.split('/')[-1]
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        res.raw.decode_content = True
        with open(dest_fp, 'wb') as fp:
            shutil.copyfileobj(res.raw, fp)
        print(f'Image successfully downloaded: {fp.name}')
    else:
        print('Image could not be fetched!')


class RemoteImageFile(object):
    def __init__(self, url, local_path=None, filename=None):
        self.__url = url
        self.__img_info = None

        if local_path:
            self.__local_dir = Path(local_path).expanduser().resolve()
        else:
            self.__local_dir = DEFAULT_IMG_DEST

    @property
    def image_info(self):
        return self.__img_info

    @image_info.setter



    @property
    def URL(self):
        return self.__url

    @property
    def local_path(self):
        return self.__local_dir.joinpath(self.__filename)

    def download(self):
        download_image(self.URL, self.local_path)
