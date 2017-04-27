import unittest
import numpy as np
from synthetic import Synthetic
from find_hot_pixels import find_hps


class TestFindHotPixels(unittest.TestCase):

    # Create random images and throw in hot pixels
    def setUp(self):
        psf = np.ones((5, 5)) / 5 ** 2
        synthetic = Synthetic(shape=(1944, 2592), background_mean=100, background_std=1.5, psf=psf, star_count=50)

        im_one = synthetic.generate_image(exposure=5)
        im_two = synthetic.generate_image(exposure=10)

        # Throw in 25 hot pixels in the same locations in both images
        self.images = add_hot_pixels([im_one, im_two], count=25)

    def tearDown(self):
        self.images = None

    def test_find_hot_pixels(self):
        hot_pixel_count = len(find_hps(self.images, sigma=3))
        self.assertEqual(hot_pixel_count, 25)


# Helper function
def add_hot_pixels(images, count):

    y, x = images[0].shape

    for c in range(count):
        hp = np.random.randint(115, 4000)
        y_pos = np.random.randint(0, y)
        x_pos = np.random.randint(0, x)

        for i in range(len(images)):
            images[i][y_pos, x_pos] = hp

    return images

if __name__ == '__main__':
    unittest.main()
