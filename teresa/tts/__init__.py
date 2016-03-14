from collections import OrderedDict

from . import svox
from . import voicerss

ENGINE_MAP = OrderedDict(
    {
        'voicerss': voicerss,
        'svox': svox
    }
)
