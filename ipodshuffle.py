from .show import show

from .sync import sync

from .set import set_

actions = {
    'show': show,
    'sync': sync,
    'set': set_,
}


if __name__ == '__main__':
    import sys

    # sync(dir_path2)

    args = {}

    action = None

    for one in sys.argv[1:]:
        k, v = one.split('=')

        if k == 'action':
            

        if ',' in v:
            value = v.split(',')
        else:
            value = v

        args[k] = value

    sync(**args)
