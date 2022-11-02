import functools
from pypattyrn.behavioral.null import Null

old_print = print

print = print


def debug(func):
    global old_print, print
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        print(args)
        print(kwargs)
        od = Null()
        if 'debug' in kwargs.keys() and kwargs['debug']:
            od = print

        return func(out_dev=od)
    return wrapper_decorator
