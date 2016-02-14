#!/usr/bin/env python3

import sys

from collections import OrderedDict

from ipodshuffle.tools import show, set_, sync

"""
'shuffle.py' is used by IPod-Shuffle-4g.
teresa may be a good name for this script, from Teresa Teng (邓丽君)
"""


modules = OrderedDict()

for _name, _module in (['show', show], ['set', set_], ['sync', sync]):
    modules[_name] = _module


class ArgumentsError(Exception):
    pass


def help_():
    # script_name = format(sys.argv[0])
    script_name = 'teresa'
    s = 'usage: {} fun=<fun> <arg1>=<value1> <arg2>=<value2> ... \n'.format(script_name) + \
        '  or : {} help\n'.format(script_name) + \
        '\n'

    s += 'All funs are:\n'
    for name, module in modules.items():
        s += '\n'
        s += '   {:<7}description:  {}\n'.format(name, module.description)
        s += module.get_help_strings(indet=10) or '\n'

    print(s, end='')


def main():
    kwargs = parse_arg()

    if 'help' in kwargs.keys() and kwargs['help']:
        help_()

    elif 'fun' in kwargs.keys():
        name = kwargs.pop('fun')
        modules[name].fun(**kwargs)

    else:
        help_()


def parse_arg():
    kwargs = {}

    for _one in sys.argv[1:]:

        if '=' not in _one:
            kwargs[_one] = True
            continue

        k, v = _one.split('=')

        if ',' in v:
            value = v.split(',')
        elif v.lower() == 'true':
            value = True
        elif v.lower() == 'false':
            value = False
        elif v.isdigit():
            value = int(v)
        else:
            value = v

        kwargs[k] = value

    return kwargs


if __name__ == '__main__':
    main()