import os
from gorila.cameramodels import BrownModel
from orex_setup import TagCamsCamera
import numpy as np
from skimage import io


__doc__ = """
Read in the raw TAGCAMS files in a directory and correct the distortion and column-to-column offset using
the gorila software package. Return an instance of a TagCamsCamera with the images loaded in."""


# specify the initial guess at the camera model (Brown Model)
# field of view of the camera (only used for querying the star catalogues)
fov = 60

# focal length terms of the camera
focal_x = 3.471329500394224e3  # pixels per mm
focal_y = 3.471331072802499e3  # pixels per mm

# the location of the principal point (place where the optical axis pierces the image plane)
princ_point_x = 1268.43051452  # pixels
princ_point_y = 949.492610414  # pixels

# distortion coefficients
# radial distortions
k1 = -0.000539524477757e3
k2 = 0.000392825359772e3
k3 = -0.000234634544288e3
# tip/tilt/prism distortions
p1 = -0.000000186449437e3
p2 = 0.000000888233963e3

# create the camera model
ncmodel = BrownModel(focal_x=focal_x, focal_y=focal_y, princpoint_x=princ_point_x, field_of_view=fov,
                     princpoint_y=princ_point_y, k1=k1, k2=k2, k3=k3, p1=p1, p2=p2,
                     # set some information for the calibration.  use_apriori indicates whether to perform an update
                     # fit of the data (True) or to re-estimate the fit from scratch (False) and estimation_parameters
                     # are the parameters to estimate
                     use_apriori=False, estimation_parameters=['intrinsic', 'single misalignment'])


def load_tagcam(directories):
    """ Load in an instance of TagCamsCamera with images from the given directory

    :param directories: The location of the raw files
    :return: A TagCamsCamera with the corrected images
    """
    images = []

    for directory in directories:
        images.extend(load_directory(directory))

    # Create an instance of the camera, adding the model and the images to be processed
    navcam = TagCamsCamera(images=images, model=ncmodel, cam_name="navcam", spacecraft_name="orex")

    return navcam


def load_directory(directory):
    """ Grab a list of all the file names to be loaded from a directory

    :param directory: The location of the raw files
    :return: A list of all file names in the directory
    """
    images = []

    # Traverse the files in the given directory
    for file in os.listdir(directory):
        file_name = os.path.join(directory, file)
        # Make sure its a file and not a directory/folder and that it has the correct extension
        if not os.path.isdir(file_name) and ".img_" in file_name:
            images.append(file_name)

    return images


def raw_2_png(source_directory, destination):
    """ Convert raw NavCam images in a directory to PNG files

    :param source_directory: The directory that holds the raw image files
    :param destination: Where you want the PNG files to be saved to
    :return:
    """
    file_names = load_directory(source_directory)
    navcam = load_tagcam(directories=[source_directory])

    for index, im in enumerate(navcam.images):
        # Correct the orientation from the raw read function
        im = np.fliplr(im)

        # Use the last 4 digits before the file extension as the identifier. They're always unique
        id_position = file_names[index].rfind('.') - 4
        f_id = file_names[index][id_position: id_position+4]
        f_name = destination + f_id + ".png"

        io.imsave(f_name, im)
