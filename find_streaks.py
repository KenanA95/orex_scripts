from load_tagcam import load_tagcam
import numpy as np
from skimage.feature import canny
from skimage.transform import probabilistic_hough_line
from matplotlib import pyplot as plt

__doc__ = """
Identify potential streaks/particles in a set of images. The NavCam2 day 100 images exhibit a large number
of streaks in the images and there is now a push to figure out the cause.

Pre-process the images with a canny edge detector and use a hough transformation to identify lines in the images.
"""


def plot_lines(lines):
    for line in lines:
        (x0, y0), (x1, y1) = line
        plt.plot((x0, x1), (y0, y1))


def distance(point_one, point_two):
    """The distance between two points"""
    x1, y1 = point_one
    x2, y2 = point_two
    return np.sqrt((x2 - x1)**2 + (y2-y1)**2)


def count_streaks(lines, dist=25):
    """ The hough transformation typically identifies multiple lines for a single streak. To count the individual
    streaks, only count lines that are a given distance from one another.


    :param lines: The lines identified by the hough transformation in format ((x0, y0), (x1, y1))
    :param dist: Distance in pixels
    :return: The number of streaks
    """
    starting_points = [l[0] for l in lines]

    # First line will always be unique
    unique_points = [starting_points[0]]

    for sp in starting_points:
        unique = True

        for point in unique_points:
            if distance(sp, point) < dist:
                unique = False

        if unique:
            unique_points.append(sp)

    return len(unique_points)


def find_streaks(image):
    """ Identify potential streaks/particles in a set of images using canny edge detector and probabilistic hough lines

    :param image: The image to look for the streaks in
    :return: The number of streaks identified in the image
    """
    # No sigma because if you smooth the image you'll lose the dim streaks
    edges = canny(image, sigma=0)

    lines = probabilistic_hough_line(edges, threshold=1, line_length=6,
                                     line_gap=1)

    if lines:
        # Plot the streaks on the image
        # plt.imshow(image, cmap='gray', interpolation='none')
        # plot_lines(lines)
        # plt.show()

        return count_streaks(lines)

    return 0

# Example usage
if __name__ == "__main__":

    directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam2/DAY100/'

    navcam = load_tagcam([directory])

    for index, im in enumerate(navcam.images):
        streak_count = find_streaks(im)
        print("Index {0}: Streak Count {1}".format(index, streak_count))
