import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve2d
from skimage.transform import downscale_local_mean
from scipy.ndimage import fourier_shift


__doc__ = """ Generate synthetic images for testing purposes.

TODO - Base star brightness off of image exposure and gain
"""


class Synthetic:

    def __init__(self, shape, background_mean, background_std, psf, star_count):
        self.height, self.width = shape
        self.background_mean = background_mean
        self.background_std = background_std
        self.star_count = star_count
        self.psf = psf

    def generate_image(self, exposure):
        image = self.generate_background()
        stars = self.generate_stars(exposure)
        image = self.place_stars_randomly(image, stars)
        image += self.gaussian_noise()
        return image

    def generate_background(self):
        pixel_count = self.width * self.height
        background = np.random.normal(self.background_mean, self.background_std, pixel_count)
        return background.reshape((self.height, self.width))

    def generate_stars(self, exposure, gain=1):
        max_dn = estimate_max_dn(exposure, gain)
        stars = []
        for index in range(self.star_count):
            star = generate_2d_gaussian(size=15, star_diameter=np.random.randint(1, 8))
            # Scale so that the brightest pixel matches the estimation
            star *= (max_dn / star.max())
            star = degrade_image(star, self.psf, downsample=4, shift_range=(-2, 2))
            star += self.background_mean
            stars.append(star)

        return stars

    def place_stars_randomly(self, image, stars):
        x_lim = image.shape[1] - stars[0].shape[0]
        y_lim = image.shape[0] - stars[0].shape[1]

        for star in stars:
            x = np.random.randint(star.shape[0], x_lim)
            y = np.random.randint(star.shape[1], y_lim)

            image[y-2:y+3, x-2:x+3] = star

        return image

    def gaussian_noise(self):
        noise = np.random.normal(size=(self.height, self.width)) * self.background_std
        return noise


def generate_2d_gaussian(size, star_diameter):
    """ Generate a 2d Gaussian as the starting point for creating a fake star to place in the image

    :param size: The size of the image
    :param star_diameter: The diameter of the 2 dimensional gaussian in the center of the image
    :return: An image with a 2d gaussian placed in the center
    """
    x = np.arange(0, size, 1, float)
    y = x[:, np.newaxis]

    x0 = y0 = (size - 1) // 2

    return np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / star_diameter ** 2)


def degrade_image(im, psf, downsample, shift_range):
    """ Degrade the 2d gaussian through a shift, convolution, and downsample to create a realistic version of what a
    star might look like in the NavCam images.

    :param im: The image of the 2d gaussian to degrade
    :param psf: The point spread function to blur the image with
    :param downsample: How much to downsample the image by
    :param shift_range: The range of pixels to choose how much shift to apply
    :return: The shifted, blurred, and downsampled image of the 2d gaussian
    """

    shift = np.random.randint(shift_range[0], shift_range[1], (1, 2))[0]

    # Add shift
    im = fourier_shift(np.fft.fftn(im), shift)
    im = np.fft.ifftn(im).real

    # Blur and downsample
    im = convolve2d(im, psf)
    im = downscale_local_mean(im, (downsample, downsample))

    return im


# TODO
def estimate_max_dn(exposure, gain=1):
    """ Using previous data, estimate how bright the star should be given the exposure time.

    :param exposure: Exposure time in seconds of the synthetic image
    :param gain: Gain of the synthetic image
    :return: The value of the brightest pixel in the star
    """
    return np.random.randint(100*exposure, 500*exposure)


# Example usage
if __name__ == "__main__":

    psf = np.ones((3, 3)) / 3**2

    synthetic = Synthetic(shape=(1944, 2592), background_mean=100, background_std=0.8, psf=psf, star_count=50)

    im_one = synthetic.generate_image(exposure=1)
    im_two = synthetic.generate_image(exposure=20)

    plt.imshow(im_one, cmap='gray', interpolation='none')
    plt.show()