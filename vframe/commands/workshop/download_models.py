"""This is a template file
"""
import hashlib
import sys
import tarfile
import urllib.request
from urllib.request import urlopen

import click

from src.utils import click_utils
from src.settings import types

# --------------------------------------------------------
# command
# --------------------------------------------------------
@click.command('')
@click.pass_context
def cli(ctx,):
  """Downloads models"""

  # ------------------------------------------------
  # imports
  
  from os.path import join
  from src.utils import logger_utils, file_utils, im_utils, display_utils
  from pathlib import Path

  from tqdm import tqdm

  from src.settings import app_cfg

  # ------------------------------------------------
  # init

  dir_out = app_cfg.DIR_MODELS_CAFFE
  file_utils.mkdirs(dir_out)

  log = logger_utils.Logger.getLogger()
  
  models = [
    {
      'name': 'MobileNet-SSD',  # https://github.com/chuanqi305/MobileNet-SSD
      'url': 'https://drive.google.com/uc?export=download&id=0B3gersZ2cHIxRm5PMWRoTkdHdHc',
      'sha256': '761c86fbae3d8361dd454f7c740a964f62975ed32f4324b8b85994edec30f6af',
      'filename': 'MobileNetSSD_deploy.caffemodel'
    },
    {
      'name': 'MobileNet-SSD',
      'url': 'https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/daef68a6c2f5fbb8c88404266aa28180646d17e0/MobileNetSSD_deploy.prototxt',
      'sha256': 'e781559c4f5beaec2a486ccd952af5b6fa408e9498761bf5f4fb80b4e9f0d25e',
      'filename': 'MobileNetSSD_deploy.prototxt'
    }
  ]

  for m in tqdm(models):
    # download
    fn = m['filename']
    fp_out = join(dir_out, fn)
    if Path(fp_out).is_file() and file_utils.sha256(fp_out) == m['sha256']:
      log.info(f'file exists: {fp_out}')
    else:
      log.info(f'downloading: {fn}')
      urllib.request.urlretrieve(m['url'], fp_out)
