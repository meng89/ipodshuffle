from . import translate as _


def add_optional_group(parser):
    return parser.add_argument_group(_('optional arguments'))


def add_args_ipod_base(parser):
    parser.add_argument('-b', dest='base', help=_('ipod base path'), metavar='<path>', required=True)


def add_args_help(parser):
    parser.add_argument('-h', '--help', action='help',  help=_('show this help message and exit'))


def str2bool(v):
    return v.lower() in ('yes', 'true', 't', '1')


def str2list(v):
    return [one for one in v.split(',') if one]
