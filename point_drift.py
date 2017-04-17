from find_streaks import load_tagcam
from extract_stars import brightest_locations, extract_locations
from scipy import ndimage
from skimage.filters import threshold_otsu
import numpy as np
from skimage.feature import register_translation


# Purpose: Point-to-point correspondence between star centroids to model the spacecraft motion
# during the launch 14 day images

def calculate_centroid(im):
    thresh = threshold_otsu(im)
    binary = im > thresh
    return ndimage.measurements.center_of_mass(binary)[::-1]


def centroid_shift(im_one, im_two, star_locations):

    stars_one = extract_locations(im_one, star_locations, size=9)
    stars_two = extract_locations(im_two, star_locations, size=9)

    x_diffs, y_diffs = [], []
    for index in range(len(stars_one)):
        c1 = calculate_centroid(stars_one[index])
        c2 = calculate_centroid(stars_two[index])

        x_diffs.append(c1[0] - c2[0])
        y_diffs.append(c1[1] - c2[1])

    return np.mean(x_diffs), np.mean(y_diffs)


# "This code gives the same precision as the FFT upsampled cross-correlation
# in a fraction of the computation time and with reduced memory requirements.
# It obtains an initial estimate of the cross-correlation peak by an FFT and
# then refines the shift estimation by upsampling the DFT only in a small neighborhood
# of that estimate by means of a matrix-multiply DFT."
def fourier_shift(im_one, im_two):
    shift, error, _ = register_translation(im_one, im_two)
    return shift, error


if __name__ == "__main__":

    nc1_directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam1/L14/'
    nc2_directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam2/L14/'

    navcam1 = load_tagcam(nc1_directory)
    navcam2 = load_tagcam(nc2_directory)

    # Locations of the 10 brightest stars according to the longest exposure image
    nc1_locations = brightest_locations(navcam1.images[-1], n=20, sigma=2)
    nc2_locations = brightest_locations(navcam2.images[-1], n=10, sigma=2)

    diffs = centroid_shift(np.array(navcam1.images[-3]).astype(float),
                           np.array(navcam1.images[-1]).astype(float), nc1_locations)

    print(diffs)
