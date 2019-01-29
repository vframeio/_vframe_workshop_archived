"""Generate hashes for files
"""

import click
import pymediainfo

from src.utils import click_utils
from src.settings import types

# --------------------------------------------------------
# command
# --------------------------------------------------------
@click.command('')
@click.option('-i', '--input', 'opt_fp_in', required=True,
  help='Path to input file or folder')
@click.option('-o', '--output', 'opt_fp_out', required=True,
  help='Path to input file or folder')
@click.option('--recursive', 'opt_recursive', is_flag=True,
  help='Path to input file or folder')
@click.option('-e', '--ext', 'opt_exts', multiple=True,
  help='Path to input file or folder')
@click.option('--size', 'opt_size', default=(640,640),
  help='Image size for detection')
@click.option('--hash/--cd .o-hash', 'opt_hash', is_flag=True,
  help='Add SHA256 hash')
@click.option('--mediainfo/--no-mediainfo', 'opt_mediainfo', is_flag=True,
  help='Add EXIF data')
@click.option('--system/--no-system', 'opt_system', is_flag=True,
  help='Add EXIF data')
@click.option('--exif/--no-exif', 'opt_exif', is_flag=True,
  help='Add EXIF data')
@click.option('--faces/--no-faces', 'opt_faces', is_flag=True,
  help='Add Face detection count')
@click.option('--objects/--no-objects', 'opt_objects', is_flag=True,
  help='Add object detection (VOC 20 classes)')
@click.pass_context
def cli(ctx, opt_fp_in, opt_fp_out, opt_recursive, opt_exts, opt_size,
  opt_hash, opt_system, opt_mediainfo, opt_exif, opt_faces, opt_objects):
  """Generate media metadata and save as CSV"""

  # ------------------------------------------------
  # imports
  from pathlib import Path

  from tqdm import tqdm
  import pandas as pd
  import cv2 as cv

  from src.processors.mediainfo import MediaInfoExtractor
  from src.utils import logger_utils, file_utils, im_utils
  
  # ------------------------------------------------
  # init

  log = logger_utils.Logger.getLogger()
  log.info('generate mediainfo')
  mediainfo_extractor = MediaInfoExtractor()
  if opt_objects:
    from src.processors.detectors import ObjectDetectorCVDNN_VOC
    object_detector = ObjectDetectorCVDNN_VOC()
  if opt_faces:
    from src.processors.detectors import DetectorDLIBHOG
    face_detector = DetectorDLIBHOG()


  # get file list
  filepaths = file_utils.get_file_list(opt_fp_in)
  if not filepaths:
    log.error(f'{fp_in} is not a valid file input. Try with "--recursive"')
    return

  # ------------------------------------------------
  # process files

  results = []
  for fp_im in tqdm(filepaths):

    result = {'fn': Path(fp_im).name}  # add filename

    # extract mediainfo
    mediainfo_result = mediainfo_extractor.extract(fp_im, 
      opt_exif=opt_exif, 
      opt_mediainfo=opt_mediainfo, 
      opt_hash=opt_hash)
    result.update(mediainfo_result)

    if opt_faces or opt_objects:
      im = cv.imread(fp_im)
      im_resized = im_utils.resize(im, width=opt_size[0], height=opt_size[1])
      
      # extract faces
      if opt_faces:
        faces_result = face_detector.detect_count(im_resized)
        result.update(faces_result)

      # extract objects
      if opt_objects:
        objects_result = object_detector.detect_count(im_resized)
        result.update(objects_result)

    # append to list of all results
    results.append(result)

  # ------------------------------------------------
  # save data

  df_results = pd.DataFrame.from_dict(results)
  df_results.index.name = 'index'
  df_results.to_csv(opt_fp_out)

  log.info(f'Processed {len(filepaths)} files')
  log.info(f'Saved data to: {opt_fp_out}')

  