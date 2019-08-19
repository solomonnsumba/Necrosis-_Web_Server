
import numpy as np
import cv2
import glob
import os
from scipy import ndimage as ndi
from skimage import color, io
from skimage.draw import circle_perimeter
from skimage.filters import threshold_otsu, gaussian_filter
from skimage.morphology import closing, square
from skimage.segmentation import clear_border
from skimage.transform import resize
from skimage.measure import label, regionprops, profile_line
from .parameters import par_dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_filtered_regions(image):
    # Given an image get the possible locations for the roots
    # Not very accurate - needs more work
    # Get threshold from image
    imggray = color.rgb2gray(image)
    n = 20  # controls gaussian kernel used for filtering
    imggray = gaussian_filter(imggray, sigma=256/(4.*n), mode='reflect')
    threshold_value = threshold_otsu(imggray)
    img_background = imggray > threshold_value

    # Close small islands in the image
    img_closed = closing(img_background, square(par_dict['PAR_CLOSING']))
    clear_border(img_closed)

    # Label roots in image
    img_labelled = label(img_closed)

    # Get the different regions
    regions = regionprops(img_labelled)
    filtered_regions = [r for r in regions if r.area > par_dict['PAR_AREA_FILTER']]
    return filtered_regions


# different from original ppd code
def process_image(image, root):
    # Process single root
    # Output root and maximum and minimum values
    img_int = root.astype(np.int)
    img_int = ndi.binary_erosion(img_int, structure=np.ones((10, 10))).astype(img_int.dtype)  # cut out edge of root
    img_int = closing(img_int, square(par_dict['PAR_CBSD_CLOSING']))

    # Create a smaller version of the image by erosion
    # This is to create a ring around the image where we can analyse it
    # img_int_b = ndi.binary_erosion(img_int, structure = np.ones(PAR_EROSION)).astype(img_int.dtype)

    # # Calculate a mask for the region
    # img_temp = np.ones_like(img_int_b)
    # img_mask = img_temp - img_int_b
    img_mask = np.logical_and(img_int, img_int)

    # Overlay mask on original image
    img = np.zeros_like(image)
    img[:, :, 0] = img_mask
    img[:, :, 1] = img_mask
    img[:, :, 2] = img_mask
    img = image * img
    # io.imsave('./cutoutsha_%d.jpg'%(int(np.random.random() * 100)), img)
    return img


def calculate_int_score(int_vals):
    # Calculate intensity average score
    val_nonzero = np.nonzero(int_vals)
    vals = int_vals[val_nonzero]
    return np.mean(vals)


# different from original ppd function
def calculate_scores_img(image, total_area):
    # Calculate scores around the circumference of image in the region of interest

    # Get size of image
    (ylen, xlen, dim) = image.shape # colored image

    NUM_INSPECTION_POINTS = ylen
    s = np.zeros((NUM_INSPECTION_POINTS))

    # Run intensity lines across the length of the image
    for i in range(NUM_INSPECTION_POINTS):
        intensity_line = profile_line(image, (0,i), (xlen,i), 1)
        red_profile = intensity_line[:, 0]
        s[i] = sum(red_profile > par_dict['PAR_INTENSITY_THRESHOLD'])

    ppd_score = sum(s)/total_area
    return ppd_score


def get_ppd_area(processed_image):
    # Get the region that is covered by PPD
    # image must be a grayscale image
    imgt1 = processed_image < par_dict['PAR_PPD_UPPER_THRESHOLD']
    imgt2 = processed_image > par_dict['PAR_PPD_LOWER_THRESHOLD']
    imgt = imgt1 * imgt2  # get intersection of two filtered images
    return imgt


def get_resize_dimensions(side, image):
    # Get reduced dimensions that maintain aspect ratio of image
    r = float(side) / image.shape[1]
    dim = (side, int(image.shape[0] * r))
    return dim


def resize_images(img_path):
    # Resize image because skimage and generally the image processing will
    # take forever with large images
    img_file_name = os.path.basename(img_path)
    img_directory = os.path.dirname(img_path)

    # par_dict['PAR_RESULTS_DIR'] = os.path.join(BASE_DIR, 'results/')
    # Create results directory if it is non-existent
    if not os.path.exists(par_dict['PAR_RESULTS_DIR']):
        os.mkdir(par_dict['PAR_RESULTS_DIR'])

    image = cv2.imread(img_path.strip('/'))
    h,w = image.shape[:2]
    if h > w and h > 600:
        dim = get_resize_dimensions(400, image)
        resized_img = cv2.resize(image, dim)
    elif w > h and w > 600:
        dim = get_resize_dimensions(600, image)
        resized_img = cv2.resize(image, dim)
    else:
        resized_img = image

    resized_img_file = os.path.join(par_dict['PAR_RESULTS_DIR'], img_file_name)
    cv2.imwrite(resized_img_file, resized_img)
    return resized_img_file


def analyze_image(image_file):
    # Main PPD analysis file
    # Saves file in results folder after processing

    img = ndi.imread(image_file)
    filtered_regions = get_filtered_regions(img)
    num_regions = len(filtered_regions)  #print num_regions
    NUM_ROOTS_PER_IMG = num_regions if num_regions < 7 else par_dict['PAR_NUM_ROOTS_PER_IMG']
    root_scores = 0.0
    if NUM_ROOTS_PER_IMG != 0:
        for i in range(NUM_ROOTS_PER_IMG):
            root = filtered_regions[i]
            [mr, mc, maxr, maxc] = root.bbox
            img_root = img[mr:maxr, mc:maxc]
            img_root_orig = np.copy(img_root)
            img_processed = process_image(img_root, root.filled_image)
            img_processed_gray = color.rgb2gray(img_processed)

            PPD_mask = get_ppd_area(img_processed_gray)
            img_root_orig = color.gray2rgb(img_root_orig)
            img_root_orig[PPD_mask] = [255, 0, 0]  # color identified PPD as red for score calculation
            ppd_score = calculate_scores_img(img_root_orig, root.filled_area)
            img_root_orig[PPD_mask] = par_dict['PAR_PPD_ANOTATION_COLOR']  # color identified PPD for visual purposes
            root_scores += ppd_score
            # cv2.putText(img_root_orig, 'AR=%2.2f%%'%(ppd_score), (int(img_root_orig.shape[0]/4),int(img_root_orig.shape[1]/2)),cv2.FONT_HERSHEY_SIMPLEX,0.5,PAR_TEXT_COLOR)
            final_root_scores = str('%2.2f %%' % ((root_scores/NUM_ROOTS_PER_IMG)*100))
            img[mr:maxr, mc:maxc] = img_root_orig
            result_file = image_file[:-4] + '_analysed.jpg'
       
        cv2.putText(img,
                    'CBSD=%2.2f %%' % ((root_scores/NUM_ROOTS_PER_IMG)*100),
                    (int(img.shape[0]/10), int(img.shape[1]/15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, par_dict['PAR_TEXT_COLOR_IMG']
                    )
        cv2.imwrite(result_file, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return img, result_file, final_root_scores
    else:
        pass




