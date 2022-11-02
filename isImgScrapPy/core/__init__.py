from __future__ import annotations
from tqdm import tqdm

PROG = 'isImgScrapPyCore'

from isImgScrapPy.core.tools.web import PageInfo


class PageSet(object):
    def __init__(
            self,
            urls,
            auto_gather_pages:bool=False,
            auto_gather_images:bool=False,
            auto_download_images:bool=False,
            progress_bar=False):
        self.__pages = []
        self.__auto_gather_images = auto_gather_images
        self.__auto_download = auto_download_images
        self.__auto_gather = auto_gather_pages
        self.__urls = urls
        self.__spent = False

        if self.__auto_gather:
            self.gather()

            if self.auto_download:
                self.download_all()

    def gather(self):
        """
        The gather function is used to gather all the information from each page.
        It takes no arguments and returns a list of PageInfo objects.

        Returns:
            A list of the pageinfo objects that were created by passing each URL provided in :param:`urls` to
            :class:`PageInfo`
        """
        if len(self.pages) == 0:
            try:
                raise RuntimeError('Pages already gathered!')
            except RuntimeError as e:
                print(e)
                return self.pages
        for url in self.urls:
            self.__pages.append(PageInfo(url))

    @property
    def spent(self):
        return self.__spent

    @property
    def auto_download(self):
        return self.__auto_download

    @auto_download.setter
    def auto_download(self, new):
        if not isinstance(new, bool):
            raise TypeError('Auto download must be a boolean.')
        if self.spent:
            raise ValueError('Auto download useless as images already downloaded.')
        self.__auto_download = new

    @property
    def auto_gather_pages(self):
        return self.__auto_gather

    @property
    def auto_gather_images(self):
        return self.__auto_gather_images

    def __download_all_w_tqdm(self):
        for page in tqdm(self.__pages, desc='Downloading all images from all pages.'):
            page.download_all()


    def download_all(self, progress_bar=False):
        self.__spent = True
        if not progress_bar:
            for page in self.__pages:
                page.download_all()
        else:
            self.__download_all_w_tqdm()

    @property
    def URLs(self):
        return self.__urls

    @property
    def pages(self):
        return self.__pages

    urls = property(lambda self: self.URLs)

    def gather_pages(self):
        for url in self.URLs:
            self.pages.append(PageInfo(url, auto_gather_images=self.auto_gather_images))

    @property
    def pages(self):
        return self.__pages

    def __repr__(self):
        name = self.__class__.__name__
        num_pages = len(self.__pages)
        return str(f"[<{name}>] | Pages Held: {num_pages}")


def get_page_set(urls):
    if not isinstance(urls, (list, tuple)):
        urls = [urls]

    return PageSet(urls)

class IsImgScrapPy(object):
    def __init__(self, page_set: PageSet, auto_gather=False, auto_download=False):
        self.__page_set = page_set

    @property
    def pages(self):
        return self.__page_set


def main(urls: (list[str] | str)):
    page_set = get_page_set(urls)
