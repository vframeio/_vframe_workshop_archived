import sys
import os
from os.path import join
from pathlib import Path

import cv2 as cv
import numpy as np
import imutils
import operator

from src.utils import im_utils, logger_utils
from src.models.bbox import BBox
from src.settings import app_cfg
from src.settings import types


class ObjectDetectorCVDNN:

  def __init__(self):
    self.log = logger_utils.Logger.getLogger()

    
class ObjectDetectorCVDNN_VOC(ObjectDetectorCVDNN):

  dnn_size = (300,300)
  dnn_mean = 127.5
  dnn_scale = 0.007843
  classes = ["background", "aeroplane", "bicycle", "bird", "boat",
  "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
  "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
  "sofa", "train", "tvmonitor"]

  def __init__(self):
    super().__init__()
    fp_prototxt = join(app_cfg.DIR_MODELS_CAFFE, 'MobileNetSSD_deploy.prototxt')
    fp_model = join(app_cfg.DIR_MODELS_CAFFE, 'MobileNetSSD_deploy.caffemodel')
    self.net = cv.dnn.readNetFromCaffe(fp_prototxt, fp_model)

  def detect_count(self, im, opt_conf=0.85):
    '''Counts number of objects in an image
    '''
    (h, w) = im.shape[:2]
    im_resized = cv.resize(im, self.dnn_size)
    blob = cv.dnn.blobFromImage(im_resized, self.dnn_scale, self.dnn_size, self.dnn_mean)
    self.net.setInput(blob)
    detections = self.net.forward()


    objects = []

    for i in np.arange(0, detections.shape[2]):
      conf = detections[0, 0, i, 2] 
      if conf > opt_conf:
        idx = int(detections[0, 0, i, 1])
        label = self.classes[idx]
        objects.append(label)
        #box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        #(startX, startY, endX, endY) = box.astype("int")
    
    object_counts = {}
    for object_name in objects:
      if object_name not in object_counts.keys():
        object_counts[object_name] = 0
      else:
        object_counts[object_name] += 1

    return object_counts



class DetectorDLIBHOG:

  pyramids = 0
  conf_thresh = 0.85

  def __init__(self):
    import dlib
    self.log = logger_utils.Logger.getLogger()
    self.detector = dlib.get_frontal_face_detector()

  def detect_count(self, im, opt_conf=0.85, opt_pyramids=0):
    '''Count the number of faces in an image
    '''
    pyramids = self.pyramids if opt_pyramids is None else opt_pyramids
    dim = im.shape[:2][::-1]
    im = im_utils.bgr2rgb(im)
    hog_results = self.detector.run(im, pyramids)
    
    num_faces = 0
    if len(hog_results[0]) > 0:
      for rect, score, direction in zip(*hog_results):
        if score > self.conf_thresh:
          num_faces += 1
          self.log.debug(f'found face: {rect}')
    
    return {'faces': num_faces}
