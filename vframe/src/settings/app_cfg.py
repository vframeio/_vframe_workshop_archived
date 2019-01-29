
from os.path import join
import logging

from src.settings import types
from src.utils import click_utils

# -----------------------------------------------------------------------------
# Enun lists used for custom Click Params
# -----------------------------------------------------------------------------

LogLevelVar = click_utils.ParamVar(types.LogLevel)

# # data_store
DATA_STORE_WORKSHOP = 'data_store_workshop'
DIR_MODELS = join(DATA_STORE_WORKSHOP,'models')
# Frameworks
DIR_MODELS_CAFFE = join(DIR_MODELS,'caffe')

# -----------------------------------------------------------------------------
# click chair settings
# -----------------------------------------------------------------------------
DIR_COMMANDS_WORKSHOP = 'commands/workshop'

# -----------------------------------------------------------------------------
# Logging options exposed for custom click Params
# -----------------------------------------------------------------------------
LOGGER_NAME = 'vframe'
LOGLEVELS = {
  types.LogLevel.DEBUG: logging.DEBUG,
  types.LogLevel.INFO: logging.INFO,
  types.LogLevel.WARN: logging.WARN,
  types.LogLevel.ERROR: logging.ERROR,
  types.LogLevel.CRITICAL: logging.CRITICAL
}
LOGLEVEL_OPT_DEFAULT = types.LogLevel.DEBUG.name

LOGFILE_FORMAT = "%(log_color)s%(levelname)-8s%(reset)s %(cyan)s%(filename)s:%(lineno)s:%(bold_cyan)s%(funcName)s() %(reset)s%(message)s"

