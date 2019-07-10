import os

_ENV_VAR = "QUIONGOSPI"
_PRODUCTION = "PRODUCTION"
_DEVELOPMENT = "DEVELOPMENT"
_LOCAL = "LOCAL"

from .base import *

if os.environ.get(_ENV_VAR) == _PRODUCTION:
    from .production import *
elif os.environ.get(_ENV_VAR) == _LOCAL:
    from .local import *
