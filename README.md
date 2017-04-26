## Introduction

Throughout my internship, image processing tasks would come and go at a quick rate. To centralize and document the code being developed, I kept all of the individual programs under a single repository. 


An in-house library was used to load the images from their native format and correct image distortion and column-to-column offsets.


## Descriptions

#### `load_tagcam.py`

Read in the raw TAGCAMS files in a directory and correct the distortion and column-to-column offset using the GORILA software package. Returns an instance of a TagCamsCamera with the images loaded in.

***


#### `synthetic_image.py`

Generate a synthetic image to mimic the NavCam images for testing purposes.

***


#### `find_hot_pixels.py`

Locate potential hot/dead pixels in the NavCam images. 

***


#### `point_drift.py`

Point-to-point correspondence using the centroids of the brightest stars to characterize motion between the launch 14 day images.

***


#### `stowcam_diff.py`

Find the differences between the launch 14 day and 3/16/17 StowCam images. The new images show a black spot on the SRC that did not previously exist. 

***


#### `find_streaks.py`

Automatically identify streaks in the day 100 NavCam images. Check for correlation between sun angle, stray light, and streak count.

***


#### `stray_light.py`

Plot the stray light in each corner of the NavCam2 day 100 images to compare to the spacecraft's sun angle 

***

