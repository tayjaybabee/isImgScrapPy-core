import imagehash

from isImgScrapPy.core.images import valid_image_type


def hash_image(img_obj):
    """
    The hash_image function accepts an image object as its argument. It returns a hash of the image's contents, which
    is calculated by converting the bytes of the flattened array to a hexadecimal string.

    Arguments:
        img_obj:
            Pass in the image object that is being hashed

    Returns:
        The hash of the image
    """
    if valid_image_type(img_obj):
        return imagehash.crop_resistant_hash(img_obj)
