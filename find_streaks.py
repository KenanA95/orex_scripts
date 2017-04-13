import os
import pickle
from orex_setup import TagCamsCamera


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
