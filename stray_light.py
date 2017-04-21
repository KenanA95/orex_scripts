from load_tagcam import load_tagcam
from find_streaks import parse_time
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

# Script purpose: Plot stray light in the image corners over time to compare with
# orex sun angle


def get_grid(arr, center, size):
    offset = int((size - 1) / 2)

    return arr[center[0] - offset:center[0] + offset + 1,
               center[1] - offset:center[1] + offset + 1]


if __name__ == "__main__":

    directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam2/DAY100/'

    navcam2 = load_tagcam(directories=[directory])

    for index, im in enumerate(navcam2.images):
        # Correct orientation
        im = np.fliplr(im)

        # Grab a datetime representation of when the exposure begins
        time = parse_time(im.obsdate)

        # Grab the average DN value of each corner. Arbitrary grid size
        top_left = get_grid(im, (15, 15), size=31).mean()
        top_right = get_grid(im, (15, 2592 - 15), size=31).mean()
        bottom_left = get_grid(im, (1944 - 15, 15), size=31).mean()
        bottom_right = get_grid(im, (1944 - 15, 2592 - 15), size=31).mean()

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
