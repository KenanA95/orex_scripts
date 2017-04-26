from load_tagcam import load_tagcam
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta


__doc__ = """Plot stray light in the image corners over time to compare with orex sun angle. The day 100 NavCam2 images
exhibit an unusual amount of stray light in the corners.

"""


def get_grid(im, center, size):
    """Extract a sub-matrix from the image array around a given point

    :param im: The image to extract the sub-matrix from
    :param center: The center of the grid to be extracted
    :param size: The diameter of the grid. Ex. size=5 -> grid=5x5
    :return: A sub-matrix from the image around the center coordinates provided
    """
    offset = int((size - 1) / 2)

    return im[center[0] - offset:center[0] + offset + 1,
              center[1] - offset:center[1] + offset + 1]


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

    # To convert the fraction to a date add it the start of the current year
    time = start_date + timedelta(days=days)

    # Adjust to UTC timezone
    time = time - timedelta(hours=6)
    return time


# Example usage
if __name__ == "__main__":

    directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam2/DAY100/'

    navcam2 = load_tagcam(directories=[directory])

    for index, im in enumerate(navcam2.images):
        # Correct orientation. Raw read function returns the image flipped
        im = np.fliplr(im)

        y, x = im.shape

        # Grab a datetime representation of when the exposure begins
        time = parse_time(im.obsdate)

        # Grab the average DN value of each corner. Arbitrary grid size
        top_left = get_grid(im, (15, 15), size=31).mean()
        top_right = get_grid(im, (15, x - 15), size=31).mean()
        bottom_left = get_grid(im, (y - 15, 15), size=31).mean()
        bottom_right = get_grid(im, (y - 15, x - 15), size=31).mean()

        plt.plot(time, top_left, 'ro')
        plt.plot(time, top_right, 'go')
        plt.plot(time, bottom_left, 'bo')
        plt.plot(time, bottom_right, 'mo')

    red_patch = mpatches.Patch(color='r', label='Top Left [0, 0]')
    green_patch = mpatches.Patch(color='g', label='Top Right ')
    blue_patch = mpatches.Patch(color='b', label='Bottom Left')
    purple_patch = mpatches.Patch(color='m', label='Bottom Right')

    plt.legend(handles=[red_patch, green_patch, blue_patch, purple_patch])
    plt.title("Corner Stray Light")
    plt.ylabel('Average DN/s')
    plt.xlabel('April 10th Time')
    plt.show()
