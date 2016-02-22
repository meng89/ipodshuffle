
def str2bool(v):
    return v.lower() in ('yes', 'true', 't', '1')


def str2list(v):
    return [one for one in v.split(',') if one]
