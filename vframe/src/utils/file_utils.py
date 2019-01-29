"""
File utilities
"""
import sys
import os
from os.path import join
import stat

from glob import glob
from pprint import pprint
import shutil
import distutils
import pathlib
from pathlib import Path
import json
import csv
import pickle
import threading
from queue import Queue
import time
import logging
import itertools
import collections

import hashlib
import pymediainfo
import click
from tqdm import tqdm
import cv2 as cv
from PIL import Image
import imutils

from src.settings import app_cfg as cfg
from src.settings import types

log = logging.getLogger(cfg.LOGGER_NAME)


# ------------------------------------------
# File I/O read/write little helpers
# ------------------------------------------
def get_file_list(fp_in, exts=['jpg', 'png'], recursive=False):
  '''Returns a list of files or a list of one file
  '''
  fp_ims = []
  fpp_in = Path(fp_in)
  if fpp_in.is_dir():
    fp_ims = glob_multi(fp_in, exts, recursive=recursive)
  elif fpp_in.is_file():
    fp_ims = [fp_in] # use single image
  return fp_ims
    

def glob_multi(dir_in, exts, recursive=False):
  files = []
  for ext in exts:
    if recursive:
      fp_glob = join(dir_in, '**/*.{}'.format(ext))
      log.info(f'glob {fp_glob}')
      files +=  glob(fp_glob, recursive=True)
    else:
      fp_glob = join(dir_in, '*.{}'.format(ext))
      files += glob(fp_glob)
  return files


def get_ext(fpp, lower=True):
  """Retuns the file extension w/o dot
  :param fpp: (Pathlib.path) filepath
  :param lower: (bool) force lowercase
  :returns: (str) file extension (ie 'jpg')
  """
  fpp = ensure_posixpath(fpp)
  ext = fpp.suffix.replace('.', '')
  return ext.lower() if lower else ext


# ---------------------------------------------------------------------
# Filepath utilities
# ---------------------------------------------------------------------

def ensure_posixpath(fp):
  """Ensures filepath is pathlib.Path
  :param fp: a (str, LazyFile, PosixPath)
  :returns: a PosixPath filepath object
  """
  if type(fp) == str:
    fpp = Path(fp)
  elif type(fp) == click.utils.LazyFile:
    fpp = Path(fp.name)
  elif type(fp) == pathlib.PosixPath:
    fpp = fp
  else:
    raise TypeError('{} is not a valid filepath type'.format(type(fp)))
  return fpp


def mkdirs(fp):
  """Ensure parent directories exist for a filepath
  :param fp: string, Path, or click.File
  """
  fpp = ensure_posixpath(fp)
  fpp = fpp.parent if fpp.suffix else fpp
  fpp.mkdir(parents=True, exist_ok=True)


def sha256(fp_in, block_size=65536):
  """Generates SHA256 hash for a file
  :param fp_in: (str) filepath
  :param block_size: (int) byte size of block
  :returns: (str) hash
  """
  sha256 = hashlib.sha256()
  with open(fp_in, 'rb') as fp:
    for block in iter(lambda: fp.read(block_size), b''):
      sha256.update(block)
  return sha256.hexdigest()
