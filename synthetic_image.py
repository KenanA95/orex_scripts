import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve2d
from skimage.transform import downscale_local_mean
from scipy.ndimage import fourier_shift


class SyntheticImage:

    def __init__(self, shape, background_mean, background_std, exposure, psf, star_count):
        self.height, self.width = shape
        self.background_mean = background_mean
        self.background_std = background_std
        self.exposure = exposure
        self.star_count = star_count
        self.psf = psf

    def generate_image(self):
        image = self.generate_background()
        stars = self.generate_stars()
        image = self.place_stars(image, stars)
        image += self.gaussian_noise()
        return image

    def generate_background(self):
        pixel_count = self.width * self.height
        background = np.random.normal(self.background_mean, self.background_std, pixel_count)
        return background.reshape((self.height, self.width))

    def generate_stars(self):

        stars = []
        for index in range(self.star_count):
            star = generate_2d_gaussian(size=15, star_diameter=np.random.randint(1, 7)) * 500
            star = degrade_image(star, self.psf, downsample=4, shift_range=(-2, 2))
            star += self.background_mean
            stars.append(star)

        return stars

    def place_stars(self, image, stars):
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
    x = np.arange(0, size, 1, float)
    y = x[:, np.newaxis]

    x0 = y0 = (size - 1) // 2

    return np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / star_diameter ** 2)


def degrade_image(im, psf, downsample, shift_range):
    shift = np.random.randint(shift_range[0], shift_range[1], (1, 2))[0]

    # Add shift
    im = fourier_shift(np.fft.fftn(im), shift)
    im = np.fft.ifftn(im).real

    # Blur and downsample
    im = convolve2d(im, psf)
    im = downscale_local_mean(im, (downsample, downsample))

    return im


# Example usage
if __name__ == "__main__":

    psf = np.ones((3, 3)) / 3**2

    synthetic = SyntheticImage(shape=(1944, 2592), background_mean=100, background_std=1.4, exposure=2,
                               psf=psf, star_count=50)

    img = synthetic.generate_image()

    plt.imshow(img, cmap='gray', interpolation='none')
    plt.show()