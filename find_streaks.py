from load_tagcam import load_tagcam
from datetime import datetime, timedelta
import numpy as np
from skimage.feature import canny
from skimage.transform import probabilistic_hough_line
from matplotlib import pyplot as plt

__doc__ = """
Identify potential streaks/particles in a set of images. The NavCam2 day 100 images exhibit a large number
of streaks in the images and there is now a push to figure out the cause.

"""


def parse_time(obsdate):
    """ Take the date from the image header and format it into a datetime object

    :param obsdate: The date in the format of year and fraction of year 2017.234324
    :return: A datetime object holding the exact date and time the exposure began
    """

    fraction = str(obsdate)[4:]
    days = float(fraction) * 365.25

    # Just in case someone uses this in 2018
    current_year = str(datetime.today().year)
    start_date = datetime.strptime('01-01-' + current_year, '%d-%m-%Y')
    time = start_date + timedelta(days=days)

    # Adjust to UTC timezone
    time = time - timedelta(hours=6)
    return time


def plot_lines(lines):
    for line in lines:
        p0, p1 = line
        plt.plot((p0[0], p1[0]), (p0[1], p1[1]))


def distance(point_one, point_two):
    """The distance between two points"""
    x1, y1 = point_one
    x2, y2 = point_two
    return np.sqrt((x2 - x1)**2 + (y2-y1)**2)


# Most of the lines repeat next to each other. Only count the lines that are not neighbors
# TODO Completely rewrite or remove entirely
def count_unique_lines(lines):

    unique_points = []

    for line in lines:
        starting_point = line[0]
        # Add the first line in the list
        if not unique_points:
            unique_points.append(starting_point)

        else:
            is_unique = True
            for point in unique_points:
                if distance(starting_point, point) < 25:
                    is_unique = False

            if is_unique:
                unique_points.append(starting_point)

    return len(unique_points)


if __name__ == "__main__":

    directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam2/DAY100/'

    navcam2 = load_tagcam(directory)

    for index, im in enumerate(navcam2.images):
        # Correct orientation
        im = np.fliplr(im)

        # No sigma because if you smooth the image you'll lose the dim streaks
        edges = canny(im, sigma=0)
        lines = probabilistic_hough_line(edges, threshold=5, line_length=7,
                                         line_gap=1)

        time = parse_time(im.obsdate)
        print("Index {0}: Streak Count {1}".format(index, count_unique_lines(lines)))

        # plt.imshow(im, cmap='gray', interpolation='none')
        # plot_lines(lines)
        # plt.show()
