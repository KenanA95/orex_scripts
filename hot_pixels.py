from load_tagcam import load_tagcam
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict


# Find the overlap of active pixels that do not move between images and do not have active neighbors


def in_bounds(coords):
    return coords[0] < 1944 and coords[1] < 2592


# Check if any of the neighboring pixels are above the active threshold
def active_neighbor(im, coords, active_threshold):
    x, y = coords

    # TODO Simplify
    neighbors = [(x, y - 1), (x + 1, y - 1), (x - 1, y - 1), (x + 1, y), (x - 1, y),
                 (x, y + 1), (x + 1, y + 1), (x - 1, y + 1)]

    for n in neighbors:
        if in_bounds(n) and im[n] >= active_threshold:
            return True

    return False


# Return a set of all x, y coordinates in an image above a given threshold
# Ignore any pixel who's direct neighbors are also above the threshold
def active_coordinates(im, active_threshold):
    x, y = np.where(im >= active_threshold)
    active_coords = list(zip(x, y))

    # Remove any coordinates that have neighbors who are active
    active_coords = [c for c in active_coords if not active_neighbor(im, c, active_threshold)]

    return set(active_coords)


# Find the overlap of active pixels between images
def active_overlap(navcam, sigma):
    active_coords = {}

    for index, im in enumerate(navcam.images):
        active_threshold = im.mean() + (sigma * im.std())
        active_coords[index] = active_coordinates(im, active_threshold)

    # This returns the intersection for the sets of active coordinates
    return list(set.intersection(*active_coords.values()))


# Get the value of every hot pixel across all images
def get_hp_values(images, overlap):
    hp_values = defaultdict(list)

    for index, ol in enumerate(overlap):
        for im in images:
            hp_values[index].append(im[ol])

    return hp_values


if __name__ == "__main__":

    directory_day100 = 'C:/Users/kalkiek/Desktop/repos/data/navcam1/DAY100/'
    directory_l14 = 'C:/Users/kalkiek/Desktop/repos/data/navcam1/L14/'

    navcam1 = load_tagcam(directories=[directory_day100])

    overlap = active_overlap(navcam1, sigma=4)

    print("Located {0} overlapping active pixels".format(len(overlap)))

    x_overlap = [o[1] for o in overlap]
    y_overlap = [o[0] for o in overlap]

    # Display the overlap on a navcam image
    plt.imshow(navcam1.images[20], cmap='gray', interpolation='nearest')
    plt.scatter(x_overlap, y_overlap, color='none', edgecolors='red', linewidths=1)
    plt.axis('off')
    plt.savefig('hot_pixels.png',)
    plt.show()
