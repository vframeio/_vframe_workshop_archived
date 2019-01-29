# --------------------------------------------------------
# command line utilities for VFRAME workshop
# (c) Adam Harvey / 2019
# https://github.com/vframeio/vframe_workshop
# --------------------------------------------------------

import click

from src.settings import app_cfg as cfg
from src.utils import logger_utils
from src.models.click_factory import ClickSimple


# click cli factory
cc = ClickSimple.create(cfg.DIR_COMMANDS_WORKSHOP)


# --------------------------------------------------------
# CLI
# --------------------------------------------------------

@click.group(cls=cc, chain=False)
@click.option('-v', '--verbose', 'verbosity', count=True, default=4, 
  show_default=True,
  help='Verbosity: -v DEBUG, -vv INFO, -vvv WARN, -vvvv ERROR, -vvvvv CRITICAL')
@click.pass_context
def cli(ctx, **kwargs):
  """\033[1m\033[94mVFRAME: Workshop Scripts\033[0m                                                
  """
  ctx.opts = {}
  logger_utils.Logger.create(verbosity=kwargs['verbosity'])  # init logger

# --------------------------------------------------------
# Entrypoint
# --------------------------------------------------------
if __name__ == '__main__':
    cli()