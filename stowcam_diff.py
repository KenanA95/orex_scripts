from find_streaks import load_tagcam
import numpy as np
from matplotlib import pyplot as plt

# Purpose: On 3/16/17 new images of the StowCam arrived. The src has a black spot, and it is unsure
# of whether it is a particulate or burn off is occurring. To get a better understanding this program
# takes the difference between the new images and the launch 14 day images.


def stowcam_diff(im, im_l14):

    # Multiply the launch 14 day images by a heliocentric factor to adjust for them being closer to the sun
    im_l14 *= 0.86133

    # Estimated saturation threshold
    saturated = im.max() * 0.7

    sat_locations = np.where(im >= saturated)
    sat_locations_l14 = np.where(im_l14 >= saturated)

    difference = abs(np.subtract(im, im_l14))

    # Set the location of the saturated areas to the average value so they don't stick out
    difference[sat_locations], difference[sat_locations_l14] = difference.mean(), difference.mean()

    # Scale the final result to 0-255
    scale = difference.max() / 255
    difference /= scale
    return difference


if __name__ == "__main__":

    directory = 'C:/Users/kalkiek/Desktop/repos/data/stowcam/3-16-17/'
    directory_l14 = 'C:/Users/kalkiek/Desktop/repos/data/stowcam/L14/'

    stowcam = load_tagcam(directory)
    stowcam_l14 = load_tagcam(directory_l14)

    if len(stowcam.images) != len(stowcam_l14.images):
        print("Incorrect number of files provided")
        exit(-1)

    for i in range(len(stowcam.images)):
        # Correct the image orientation
        im = np.fliplr(np.flipud(stowcam.images[i]))
        im_l14 = np.fliplr(np.flipud(stowcam_l14.images[i]))

        diff = stowcam_diff(im, im_l14.astype(float))
        print(diff.mean(), diff.std())
        plt.imshow(diff, cmap='gray')
        plt.show()