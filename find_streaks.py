import os
import pickle
from orex_setup import TagCamsCamera
from datetime import datetime, timedelta
import numpy as np
from skimage.feature import canny
from skimage.transform import probabilistic_hough_line
from matplotlib import pyplot as plt

# Script purpose: Identify potential streaks/particles in a set of images


# Load in an instance of TagCamsCamera with images from the given directory
def load_tagcam(directory):

    # Brown Model to correct distortion with the navcam specs provided
    ncmodel = pickle.load(open("ncmodel.p", "rb"))

    images = []

    # Traverse the files in the given directory
    for file in os.listdir(directory):
        file_name = os.path.join(directory, file)
        # Make sure its a file and not a directory/folder
        if not os.path.isdir(file_name):
            images.append(file_name)

    # Create an instance of the camera, adding the model and the images to be processed
    navcam = TagCamsCamera(images=images, model=ncmodel, cam_name="navcam", spacecraft_name="orex")

    return navcam


# Dates comes in the format 2017.234324 have to convert that fraction
# into a precise date
def parse_time(obsdate):

    fraction = str(obsdate)[4:]
    days = float(fraction) * 365.25

    # Just in case someone uses this in 2018
    current_year = str(datetime.today().year)
    start_date = datetime.strptime('01-01-' + current_year, '%d-%m-%Y')
    time = start_date + timedelta(days=days)

    # Adjust to UTC timezone
    time = time - timedelta(hours=6)
    return time


def draw_lines(lines):
    for line in lines:
        p0, p1 = line
        plt.plot((p0[0], p1[0]), (p0[1], p1[1]))


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
        print("Index {0}: Line Count {1}".format(index, len(lines)))

        plt.imshow(im, cmap='gray', interpolation='none')
        draw_lines(lines)
        plt.show()