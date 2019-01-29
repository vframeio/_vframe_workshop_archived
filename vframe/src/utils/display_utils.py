import sys

import cv2 as cv

from src.utils.logger_utils import Logger


log = Logger.getLogger()

def handle_keyboard(delay_amt=1):
  '''Used with cv.imshow('title', image) to wait for keyboard press
  '''
  while True:
    k = cv.waitKey(delay_amt) & 0xFF
    if k == 27 or k == ord('q'):  # ESC
      cv.destroyAllWindows()
      sys.exit()
    elif k == 32 or k == 83:  # 83 = right arrow
      break
    elif k != 255:
      log.debug(f'k: {k}')
