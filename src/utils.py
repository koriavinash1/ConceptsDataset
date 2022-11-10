import cv2
from imgaug import augmenters as iaa
import numpy as np


class CreateObject(object):
    def __init__(self, height, width):
        self.height = height 
        self.width = width
        self.affine = iaa.Sequential([
                            iaa.Affine(rotate=(-25, 25)),
                            iaa.AdditiveGaussianNoise(scale=(10, 60)),
                            iaa.Crop(percent=(0, 0.2))
                        ]) 

    def create_square(H, W):
        img = np.uint8(np.ones((H, W, 3)))
        color = tuple(np.random.randint(0, 255, 3))

        img = cv2.rectangle(img, 
                pt1=H//2, 
                pt2=W//2, 
                color=color, 
                thickness=-1)
        return img


    def create_triangle():
        pass


    def create_star():
        pass


    def create_circle():
        pass 

    def create_capsule():
        pass 


    def create_ellipse():
        pass 