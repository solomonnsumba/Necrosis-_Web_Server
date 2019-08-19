"""
Parameters controlling the detection of PPD

ver. 20160116
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


PAR_CLOSING = 3  # controls filtering in image preprocessing
PAR_AREA_FILTER = 5000  # controls the thresholding area used to filter out the roots from the image. Depends on initial size of image used
PAR_EROSION = (50, 50)  # controls erosion parameter to select circular region of interest for PPD
PAR_CBSD_CLOSING = 30
PAR_INTENSITY_THRESHOLD = 254.0  # controls threshold for profile line that determines if PPD exists
PAR_PPD_THICKNESS = 6  # controls how much evidence of PPD to consider (i.e. how many *red* pixels are seen)
PAR_PPD_UPPER_THRESHOLD = 0.57  # controls the thresholding of what we consider as PPD on the cross section of the image. Its a float image so pixel values vary from 0 - 1
PAR_PPD_LOWER_THRESHOLD = 0.1  # controls lower threshold for PPD i.e. eliminates counting mask as part of PPD
PAR_IMG_SOURCE_DIR = './test_source/'
PAR_RESULTS_DIR = ''  # not used yet
PAR_NUM_ROOTS_PER_IMG = 1  # represents number of roots in an image (controls how many regions should be identified in each image)
PAR_TEXT_COLOR = (0, 0, 0)  # REDUNDANT
PAR_PPD_ANOTATION_COLOR = [150, 85, 0]
PAR_TEXT_COLOR_IMG = (255, 255, 255)  # color of average score for the whole image

defaults_dict = dict(
    PAR_RESULTS_DIR=os.path.join(BASE_DIR, 'media/uploads/results'),
    PAR_IMG_SOURCE_DIR='./test_source/',
    PAR_CLOSING=3,
    PAR_AREA_FILTER=5000,
    PAR_EROSION=(50, 50),
    PAR_CBSD_CLOSING=30,
    PAR_INTENSITY_THRESHOLD=254.0,
    PAR_PPD_THICKNESS=6,
    PAR_PPD_UPPER_THRESHOLD=0.57,
    PAR_PPD_LOWER_THRESHOLD=0.1,
    PAR_NUM_ROOTS_PER_IMG=1,
    PAR_TEXT_COLOR_IMG=(255, 255, 255),
    PAR_PPD_ANOTATION_COLOR=[150, 85, 0])
    
par_dict = defaults_dict.copy()
