from load_tagcam import load_tagcam
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict


__doc__ = """
Check for hot/dead pixels in the NavCam images. Hot pixels are pixels that incorrectly show activity.
Since the error exists on the hardware side, hot pixels will always remain in the same location. The idea is to
find an overlap of pixels that show activity in every image that are not a part of a star

One idea that was implemented and later retracted was to identify the stars in the image and exclude their projected
locations as potential hot pixels. The issue is that most of the images from a given set do not point at the
same location. One possible solution is to identify the location of every single image, but that can be very
computationally expensive and does not seem to produce better results.

"""


def in_bounds(coords):
    """Make sure the coordinate being evaluated are actually in the image. If an active pixel is found on the very edge
     of an image, it's neighbor will be out of bounds

    :param coords: The x, y coordinates to check
    :return: True if the coordinates lie within the active image. False otherwise
    """
    return coords[0] < 1944 and coords[1] < 2592


def active_neighbor(im, coords, active_threshold):
    """Check if any of the neighboring pixels are above an active threshold

    :param im: The image
    :param coords: Coordinates of the pixel to check the neigboring values
    :param active_threshold: The integer cutoff for what is considered 'active'
    :return: True if the pixel has a neighbor above the threshold. False otherwise
    """
    x, y = coords

    # Probably a better way to do this...
    neighbors = [(x, y - 1), (x + 1, y - 1), (x - 1, y - 1), (x + 1, y), (x - 1, y),
                 (x, y + 1), (x + 1, y + 1), (x - 1, y + 1)]

    for n in neighbors:
        if in_bounds(n) and im[n] >= active_threshold:
            return True

    return False


def active_coordinates(im, active_threshold):
    """Find the coordinates of every pixel above a given threshold. Ignore any who's neighbors are also active

    :param im: The image to check for active coordinates
    :param active_threshold: The integer cutoff for what is considered 'active'
    :return: The set of coordinates above the active threshold with no active neighbors
    """

    x, y = np.where(im >= active_threshold)
    active_coords = list(zip(x, y))

    # Remove any coordinates that have neighbors who are active
    active_coords = [c for c in active_coords if not active_neighbor(im, c, active_threshold)]

    return set(active_coords)


def active_overlap(navcam, sigma):
    """ Find the intersection of the active coordinates for every image in the set

    :param navcam: Instance of a TagCamsCamera that holds the corrected images
    :param sigma: Number of deviations above the mean used to define the active threshold
    :return: The overlapping coordinates of potential hot pixels for every image in the set
    """

    active_coords = {}

    for index, im in enumerate(navcam.images):
        active_threshold = im.mean() + (sigma * im.std())
        active_coords[index] = active_coordinates(im, active_threshold)

    # Return the intersection for the sets of active coordinates
    return list(set.intersection(*active_coords.values()))


def get_hp_values(images, hp_locs):
    """Get the value the hot pixels across all images for comparison statistics

    :param images: The images to grab the hot pixel value from
    :param hp_locs: The locations of the hot pixels
    :return: A dictionary that holds a list of the hot pixel values for every image
    """
    hp_values = defaultdict(list)

    for index, loc in enumerate(hp_locs):
        for im in images:
            hp_values[index].append(im[loc])

    return hp_values


# Example usage
if __name__ == "__main__":

    directory_day100 = 'C:/Users/kalkiek/Desktop/repos/data/navcam1/DAY100/'
    directory_l14 = 'C:/Users/kalkiek/Desktop/repos/data/navcam1/L14/'

    navcam1 = load_tagcam(directories=[directory_day100])

    overlap = active_overlap(navcam1, sigma=4)

    print("Located {0} overlapping active pixels".format(len(overlap)))

    x_overlap = [o[1] for o in overlap]
    y_overlap = [o[0] for o in overlap]

    # Circle the locations on an empty image so that the people can overlay it onto new images
    # To save the image in exact pixel size use figure.set_size_inches(). Nothing else works
    # consistently

    empty_image = np.zeros((2004, 2752))
    fig = plt.figure(frameon=False)
    fig.set_size_inches(27.52, 20.04)

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(empty_image, aspect='normal', cmap='gray')

    # Adjust for the dark pixel columns that surround the NavCam images
    ax.scatter(np.add(x_overlap, 144), np.add(y_overlap, 54), color='none', edgecolors='red', linewidths=1)
    fig.savefig('hot_pixels.png', dpi=100)
