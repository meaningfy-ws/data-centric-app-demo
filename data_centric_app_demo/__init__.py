import pathlib
from pydantic import ConfigDict

DEFAULT_MODEL_CONFIG = ConfigDict(extra='forbid',
                                  strict=True)

STRICT_MODEL_CONFIG = ConfigDict(extra='forbid',
                                  strict=True,
                                  validate_assignment=True,
                                  revalidate_instances='always',
                                  validate_default=True,
                                  validate_return=True)


__version__ = "0.0.1"
__root_path__ = pathlib.Path(__file__).parent.resolve()