import unittest
import numpy as np
from synthetic import Synthetic
from find_streaks import find_streaks
from skimage.draw import line_aa


class TestFindStreaks(unittest.TestCase):

    def setUp(self):
        # Create a fake image and add 5 streaks
        psf = np.ones((5, 5)) / 5 ** 2
        synthetic = Synthetic(shape=(1000, 1000), background_mean=100, background_std=0.0001, psf=psf, star_count=25)
        image = synthetic.generate_image(exposure=5)
        self.image = add_streaks(image, count=5)

    def tearDown(self):
        self.image = None

    def test_find_streaks(self):
        streak_count = find_streaks(self.image)
        self.assertEqual(streak_count, 5)


# Helper functions


def place_streak(image, length, value):
    y, x = image.shape

    y_start = np.random.randint(0, y-length)
    x_start = np.random.randint(0, x-length)
    rr, cc, val = line_aa(y_start, x_start, y_start+length, x_start+length)
    image[rr, cc] = val * value
    return image


def add_streaks(image, count):

    streak_value = 1500

    for c in range(count):
        length = np.random.randint(7, 25)
        image = place_streak(image, length, streak_value)

    return image


if __name__ == '__main__':
    unittest.main()
