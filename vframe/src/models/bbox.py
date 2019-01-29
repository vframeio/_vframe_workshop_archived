"""WIP, a class for modeling and manipulating bounding box data
"""

import math
import random

from dlib import rectangle as dlib_rectangle
import numpy as np


class BBoxPoint:

  def __init__(self, x, y):
    self._x = x
    self._y = y

  @property
  def x(self):
    return self._x
  
  @property
  def y(self):
    return self._y
  
  def offset(self, x, y):
    return (self._x + x, self._y + y)

  def tuple(self):
    return (self._x, self._y)


class BBox:

  def __init__(self, x1, y1, x2, y2):
    """Represents a bounding box and provides methods for accessing and modifying
    All values are normalized unless otherwise specified
    :param x1: normalized left coord
    :param y1: normalized top coord
    :param x2: normalized right coord
    :param y2: normalized bottom coord
    """
    self._x1 = x1
    self._y1 = y1
    self._x2 = x2
    self._y2 = y2
    self._width = x2 - x1
    self._height = y2 - y1
    self._cx = x1 + (self._width / 2)
    self._cy = y1 + (self._height / 2)
    self._tl = (x1, y1)
    self._br = (x2, y2)
    self._rect = (self._x1, self._y1, self._x2, self._y2)
    self._area = self._width * self._height  # as percentage

  @property
  def area(self):
    return self._area
  
  @property
  def pt_tl(self):
    return self._tl

  @property
  def pt_br(self):
    return self._br

  @property
  def x(self):
    return self._x1
  
  @property
  def y(self):
    return self._y1

  @property
  def x1(self):
    return self._x1
  
  @property
  def y1(self):
    return self._y1


  @property
  def x2(self):
    return self._x2
  
  @property
  def y2(self):
    return self._y2
  
  @property
  def height(self):
    return self._height

  @property
  def width(self):
    return self._width

  @property
  def h(self):
    return self._height

  @property
  def w(self):
    return self._width

  @property
  def cx(self):
    return self._cx

  @property
  def cy(self):
    return self._cy
  
  # # -----------------------------------------------------------------
  # # Utils

  def contains(self, pt_norm):
    '''Returns Checks if this BBox contains the normalized point
    :param pt: (int|float, int|float) x, y
    :returns (bool)
    '''
    x, y = pt_norm
    return (x > self._x1 and x < self._x2 and y > self._y1 and y < self._y2)

  def distance(self, b):
    a = self
    dcx = self._cx - b.cx
    dcy = self._cy - b.cy
    d = int(math.sqrt(math.pow(dcx, 2) + math.pow(dcy, 2)))
    return d


  # -----------------------------------------------------------------
  # Modify

  def jitter(self, amt):
    '''Jitters BBox in x,y,w,h values. Used for face feature extraction
    :param amt: (float) percentage of BBox for maximum translation
    :returns (BBox)
    '''
    w = self._width + (self._width * random.uniform(-amt, amt))
    h = self._height + (self._height * random.uniform(-amt, amt))
    cx = self._cx + (self._cx * random.uniform(-amt, amt))
    cy = self._cy + (self._cy * random.uniform(-amt, amt))
    x1, y1 = np.clip((cx - w/2, cy - h/2), 0.0, 1.0)
    x2, y2 = np.clip((cx + w/2, cy + h/2), 0.0, 1.0)
    return BBox(x1, y1, x2, y2)

  def expand(self, per):
    """Expands BBox by percentage
    :param per: (float) percentage to expand 0.0 - 1.0
    :param dim: (int, int) image width, height
    :returns (BBox) expanded
    """
    # expand
    dw, dh = [(self._width * per), (self._height * per)]
    r = list(np.array(self._rect) + np.array([-dw, -dh, dw, dh]))
    # threshold expanded rectangle
    r[0] = max(r[0], 0.0)
    r[1] = max(r[1], 0.0)
    r[2] = min(r[2], 1.0)
    r[3] = min(r[3], 1.0)
    return BBox(*r)

  def expand_dim(self, amt, bounds):
    """Expands BBox within dim
    :param box: (tuple) left, top, right, bottom
    :param bounds: (tuple) width, height
    :returns (BBox) in pixel dimensions
    """
    # expand
    r = list( (np.array(self._rect) + np.array([-amt, -amt, amt, amt])).astype('int'))
    # outliers
    oob = list(range(4))
    oob[0] = min(r[0], 0)
    oob[1] = min(r[1], 0)
    oob[2] = bounds[0] - r[2]
    oob[3] = bounds[1] - r[3]
    oob = np.array(oob)
    oob[oob > 0] = 0
    # absolute amount
    oob = np.absolute(oob)
    # threshold expanded rectangle
    r[0] = max(r[0], 0)
    r[1] = max(r[1], 0)
    r[2] = min(r[2], bounds[0])
    r[3] = min(r[3], bounds[1])
    # redistribute oob amounts
    oob = np.array([-oob[2], -oob[3], oob[0], oob[1]])
    r = np.add(np.array(r), oob)
    # find overage
    oob[0] = min(r[0], 0)
    oob[1] = min(r[1], 0)
    oob[2] = bounds[0] - r[2]
    oob[3] = bounds[1] - r[3]
    oob = np.array(oob)
    oob[oob > 0] = 0
    oob = np.absolute(oob)
    if np.array(oob).any():
      m = np.max(oob)
      adj = np.array([m, m, -m, -m])
      # print(adj)
      r = np.add(np.array(r), adj)

    return BBox(*r)  # updats all BBox values


  # -----------------------------------------------------------------
  # Convert to

  def to_square(self, bounds):
    '''Forces bbox to square dimensions
    :param bounds: (int, int) w, h of the image
    :returns (BBox) in square ratio
    '''

  def to_dim(self, dim):
    """scale is (w, h) is tuple of dimensions"""
    w, h = dim
    rect = list((np.array(self._rect) * np.array([w, h, w, h])).astype('int'))
    return BBox(*rect)

  def normalize(self, rect, dim):
    w, h = dim
    x1, y1, x2, y2 = rect
    return (x1 / w, y1 / h, x2 / w, y2 / h)

  # -----------------------------------------------------------------
  # Format as

  def to_xyxy(self):
    """Converts BBox back to x1, y1, x2, y2 rect"""
    return (self._x1, self._y1, self._x2, self._y2)

  def to_xywh(self):
    """Converts BBox back to haar type"""
    return (self._x1, self._y1, self._width, self._height)

  def to_trbl(self):
    """Converts BBox to CSS (top, right, bottom, left)""" 
    return (self._y1, self._x2, self._y2, self._x1)

  def to_dlib(self):
    """Converts BBox to dlib rect type"""
    return dlib_rectangle(self._x1, self._y1, self._x2, self._y2)

  def to_yolo(self):
    """Converts BBox to normalized center x, center y, w, h"""
    return (self._cx, self._cy, self._width, self._height)


  # -----------------------------------------------------------------
  # Create from

  @classmethod
  def from_xywh_norm_dim(cls, x, y, w, h, dim):
    """Converts w, y, w, h to normalized BBox
    :returns BBox
    """
    x1, y1 = (x * dim[0], y * dim[1])
    x2, y2 = (w * dim[0]) + x1, (h * dim[1]) + y1
    rect = cls.normalize(cls, (x1, y1, x2, y2), dim)
    return cls(*rect)

  @classmethod
  def from_xyxy_dim(cls, x1, y1, x2, y2, dim):
    """Converts x1, y1, w, h to BBox and normalizes
    :returns BBox
    """
    rect = cls.normalize(cls, (x1, y1, x2, y2), dim)
    return cls(*rect)

  @classmethod
  def from_xywh_dim(cls, x, y, w, h, dim):
    """Converts x1, y1, w, h to BBox and normalizes
    :param rect: (list) x1, y1, w, h
    :param dim: (list) w, h
    :returns BBox
    """
    rect = cls.normalize(cls, (x, y, x + w, y + h), dim)
    return cls(*rect)

  @classmethod
  def from_xyxy(cls, x1, y1, x2, y2):
    """Converts x1, y1, x2, y2 to BBox
    same as constructure but zprovided for conveniene
    """
    return cls(x1, y1, x2, y2)

  @classmethod
  def from_xywh(cls, x, y, w, h):
    """Converts x1, y1, w, h to BBox
    :param rect: (list) x1, y1, w, h
    :param dim: (list) w, h
    :returns BBox
    """
    return cls(x, y, x+w, y+h)

  @classmethod
  def from_css(cls, rect, dim):
    """Converts rect from CSS (top, right, bottom, left) to BBox
    :param rect: (list) x1, y1, x2, y2
    :param dim: (list) w, h
    :returns BBox
    """
    rect = (rect[3], rect[0], rect[1], rect[2])
    rect = cls.normalize(cls, rect, dim)
    return cls(*rect)

  @classmethod
  def from_dlib_dim(cls, rect, dim):
    """Converts dlib.rectangle to BBox
    :param rect: (list) x1, y1, x2, y2
    :param dim: (list) w, h
    :returns dlib.rectangle
    """ 
    rect = (rect.left(), rect.top(), rect.right(), rect.bottom())
    rect = cls.normalize(cls, rect, dim)
    return cls(*rect) 

  def __str__(self):
    return f'BBox: ({self._x1},{self._y1}), ({self._x2}, {self._y2}), width:{self._width}, height:{self._height}'

  def __repr__(self):
    return f'BBox: ({self._x1},{self._y1}), ({self._x2}, {self._y2}), width:{self._width}, height:{self._height}'

  def str(self):
    """Return BBox as a string "x1, y1, x2, y2" """
    return self.as_box()

