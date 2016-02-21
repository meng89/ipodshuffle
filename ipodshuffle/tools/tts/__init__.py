from collections import OrderedDict

from . import voicerss
from . import sovx


ENGINE_MAP = OrderedDict(
    {
        'voicerss': voicerss,
        'sovx': sovx
    }
)
