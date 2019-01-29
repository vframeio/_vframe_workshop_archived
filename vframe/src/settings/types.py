from enum import Enum

def find_type(name, enum_type):
  for enum_opt in enum_type:
    if name == enum_opt.name.lower():
      return enum_opt
  return None

  

class CVBackend(Enum):
  """OpenCV 3.4.2+ DNN target type"""
  DEFAULT, HALIDE, INFER_ENGINE, OPENCV = range(4)

class CVTarget(Enum):
  """OpenCV 3.4.2+ DNN backend processor type"""
  CPU, OPENCL, OPENCL_FP16, MYRIAD = range(4)

class HaarCascade(Enum):
  FRONTAL, ALT, ALT2, PROFILE = range(4)


# ---------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------

class DataStore(Enum):
  """Storage devices. Paths are symlinked to root (eg /data_store_nas)"""
  NAS, HDD, SSD, S3 = range(4)

# ---------------------------------------------------------------------
# Logger, monitoring
# --------------------------------------------------------------------

class LogLevel(Enum):
  """Loger vebosity"""
  DEBUG, INFO, WARN, ERROR, CRITICAL = range(5)


# ---------------------------------------------------------------------
# Metadata types
# --------------------------------------------------------------------

class Metadata(Enum):
  IDENTITY, FILE_RECORD, FACE_VECTOR, FACE_POSE, \
    FACE_ROI, FACE_LANDMARK_2D_68, FACE_LANDMARK_2D_5,FACE_LANDMARK_3D_68, \
    FACE_ATTRIBUTES = range(9)

class Dataset(Enum):
  LFW, VGG_FACE2, MSCELEB, UCCS, UMD_FACES, SCUT_FBP, UCF_SELFIE, UTK, \
    CASIA_WEBFACE, AFW, PUBFIG83, HELEN, PIPA, MEGAFACE, BRAINWASH, IMDB_WIKI = range(16)


# ---------------------------------------------------------------------
# Face analysis types
# --------------------------------------------------------------------
class FaceDetectNet(Enum):
  """Scene text detector networks"""
  HAAR, DLIB_CNN, DLIB_HOG, CVDNN, MTCNN_TF, MTCNN_PT, MTCNN_CAFFE = range(7)

class FaceExtractor(Enum):
  """Type of face recognition feature extractor"""
  # TODO deprecate DLIB resnet and use only CVDNN Caffe models
  DLIB, VGG = range(2)

class FaceLandmark2D_5(Enum):
  DLIB, MTCNN = range(2)

class FaceLandmark2D_68(Enum):
  DLIB, FACE_ALIGNMENT = range(2)

class FaceLandmark3D_68(Enum):
  FACE_ALIGNMENT = range(1)
  
class FaceEmotion(Enum):
  # Map these to text strings for web display
  NEUTRAL, HAPPY, SAD, ANGRY, FRUSTURATED = range(5)

class FaceBeauty(Enum):
  # Map these to text strings for web display
  AVERAGE, BELOW_AVERAGE, ABOVE_AVERAGE = range(3)

class FaceYaw(Enum):
  # Map these to text strings for web display
  FAR_LEFT, LEFT, CENTER, RIGHT, FAR_RIGHT = range(5)

class FacePitch(Enum):
  # Map these to text strings for web display
  FAR_DOWN, DOWN, CENTER, UP, FAR_UP = range(5)

class FaceRoll(Enum):
  # Map these to text strings for web display
  FAR_DOWN, DOWN, CENTER, UP, FAR_UP = range(5)

class FaceAge(Enum):
  # Map these to text strings for web display
  CHILD, TEENAGER, YOUNG_ADULT, ADULT, MATURE_ADULT, SENIOR = range(6)

class Confidence(Enum):
  # Map these to text strings for web display
  VERY_LOW, LOW, MEDIUM, MEDIUM_HIGH, HIGH, VERY_HIGH = range(6)