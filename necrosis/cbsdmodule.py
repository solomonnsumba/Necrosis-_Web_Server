
from cbsdanalyzer import *

def analyze(path):
    resized_img_path = resize_images(path)
    return analyze_image(resized_img_path)

def gauge(path):
    print path
    f = analyze(path)
