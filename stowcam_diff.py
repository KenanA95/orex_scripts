from load_tagcam import load_tagcam
import numpy as np
from matplotlib import pyplot as plt

# Purpose: On 3/16/17 new images of the StowCam arrived. The src has a black spot, and it is unsure
# of whether it is a particulate or burn off is occurring. To get a better understanding this program
# takes the difference between the new images and the launch 14 day images.


def stowcam_diff(im, im_l14):

    # Multiply the launch 14 day images by a heliocentric factor to adjust for them being closer to the sun
    im_l14 *= 0.86133

    # Estimated saturation threshold
    saturated = im.max() * 0.75
    sat_locations = np.where(im >= saturated)
    sat_locations_l14 = np.where(im_l14 >= saturated)

    difference = abs(np.subtract(im, im_l14))

    # Set the location of the saturated areas to the average value so they don't stick out
    difference[sat_locations], difference[sat_locations_l14] = difference.mean(), difference.mean()

    # Scale the final result to 0-255
    scale = difference.max() / 255
    difference /= scale
    return difference


# We know that there is an increase of illumination on the src from the right to the left of the image
# If burn off is occurring, there will be a greater difference DN as we move along the src
# To test for this we compare the differences of 'panels' across the image of size 70x170
def get_panels(im):
    top_panels, bottom_panels = [], []

    for index in range(200, len(im)-200, 70):
        top_panels.append(im[800:970, index:index + 70])
        bottom_panels.append(im[1054:1224, index:index+70])

    return top_panels, bottom_panels


# TODO: Refactor
# Separate according to bayer filter color and plot the difference across the image
def plot_panel_diff(difference_image):

    avgs, stds = {'r': [], 'b': [], 'g': []}, {'r': [], 'b': [], 'g': []}
    top_panels, bottom_panels = get_panels(difference_image)

    for index in range(len(top_panels)):
        top, bottom = top_panels[index], bottom_panels[index]

        red = top[::2, ::2]
        blue = top[1::2, 1::2]
        green_odd = top[1::2, ::2]
        green_even = top[::2, 1::2]
        green = np.concatenate((green_even.ravel(), green_odd.ravel()))

        avgs['r'].append(red.mean())
        stds['r'].append(red.std())

        avgs['b'].append(blue.mean())
        stds['b'].append(blue.std())

        avgs['g'].append(green.mean())
        stds['g'].append(green.std())

    index = [i for i in range(len(avgs['b']))]

    plt.xlabel('Panel Top Section #')
    plt.ylabel('Average DN Difference (Left to Right)')
    plt.errorbar(index, avgs['b'], yerr=np.divide(stds['b'], 2), c='b')
    plt.errorbar(index, avgs['g'], yerr=np.divide(stds['g'], 2), c='g')
    plt.errorbar(index, avgs['r'], yerr=np.divide(stds['r'], 2), c='r')
    plt.show()


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

        plot_panel_diff(diff)
