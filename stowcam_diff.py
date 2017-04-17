from find_streaks import load_tagcam


# Purpose: On 3/16/17 new images of the StowCam arrived. The src has a black spot, and it is unsure
# of whether it is a particulate or burn off is occurring. To get a better understanding this program
# takes the difference between the new images and the launch 14 day images.


if __name__ == "__main__":

    directory = 'C:/Users/kalkiek/Desktop/repos/data/stowcam/3-16-17/'
    directory_l14 = 'C:/Users/kalkiek/Desktop/repos/data/stowcam/L14/'

    stowcam = load_tagcam(directory)
    stowcam_l14 = load_tagcam(directory_l14)