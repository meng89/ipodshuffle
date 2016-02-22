from collections import OrderedDict

from . import sovx
from . import voicerss

ENGINE_MAP = OrderedDict(
    {
        'voicerss': voicerss,
        'sovx': sovx
    }
)
