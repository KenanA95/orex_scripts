import numpy as np


class SyntheticImage:

    def __init__(self, shape, background_mean, background_std, exposure, star_count):
        self.height, self.width = shape
        self.background_mean = background_mean
        self.background_std = background_std
        self.exposure = exposure
        self.star_count = star_count
        self.image = np.zeros(shape)

    def generate_background(self):
        pixel_count = self.width * self.height
        background = np.random.normal(self.background_mean, self.background_std, pixel_count)
        return background.reshape((self.height, self.width))