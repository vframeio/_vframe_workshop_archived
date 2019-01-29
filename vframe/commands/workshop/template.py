"""This is a template file
"""
import click

from src.utils import click_utils
from src.settings import types

# --------------------------------------------------------
# command
# --------------------------------------------------------
@click.command('')
@click.option('-i', '--input', 'opt_fp_in',
  help='Path to input file or folder')
@click.option('-o', '--output', 'opt_fp_out',
  help='Path to input file or folder')
@click.pass_context
def cli(ctx, opt_fp_in, opt_fp_out):
  """(your command description)"""

  # ------------------------------------------------
  # imports

  from src.utils import logger_utils, file_utils, im_utils, display_utils
  from pathlib import Path

  from tqdm import tqdm
  import cv2 as cv

  # ------------------------------------------------
  # init

  log = logger_utils.Logger.getLogger()
  log.info('template')
  log.debug('template')
  log.warn('template')
  log.error('template')