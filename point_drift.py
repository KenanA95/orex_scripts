from find_streaks import load_tagcam


# Purpose: Point-to-point correspondence between star centroids to model the spacecraft motion
# during the launch 14 day images


if __name__ == "__main__":

    nc1_directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam1/L14/'
    nc2_directory = 'C:/Users/kalkiek/Desktop/repos/data/navcam2/L14/'

    navcam1 = load_tagcam(nc1_directory)
    navcam2 = load_tagcam(nc2_directory)
