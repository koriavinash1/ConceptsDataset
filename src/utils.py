import cv2
from imgaug import augmenters as iaa
from matplotlib.patches import RegularPolygon
import numpy as np
import math

class CreateObject(object):
    def __init__(self, height, width):
        self.height = height 
        self.width = width
        self.max_object = self.height//4
        self.transform = iaa.Sequential([
                            iaa.Affine(rotate=(-180, 180),
                                        translate_percent={"x": (-0.38, 0.38), "y": (-0.38, 0.38)},
                                        shear=(-25, 25)),
                            iaa.AdditiveGaussianNoise(scale=(10, 60)),
                        ]) 


        self.objects = {'circle': self.create_circle,
                        'square': self.create_square,
                        'hexagon': self.create_hex,
                        'ellipse': self.create_ellipse,
                        'capsule': self.create_capsule,
                        'triangle': self.create_ellipse}


    def create_canvas(self, background-(255, 255, 255)):
        img = np.uint8(np.zeros((self.height, self.width, 3)))
        img[:,:, 0] = background[0]
        img[:,:, 1] = background[1]
        img[:,:, 2] = background[2]
        return img 


    def create_square(self, background=(255, 255, 255)):
        img = self.create_canvas(background)
        object_height = np.random.randint(0, self.max_object)
        object_width = np.random.randint(0, self.max_object)

        start_point = (self.width//2 - object_width//2, self.height//2 - object_height//2)
        end_point = (self.width//2 + object_width//2, self.height//2 + object_height//2)
        color = tuple(np.random.randint(0, 255, 3))
        img = cv2.rectangle(img, 
                pt1=start_point, 
                pt2=end_point, 
                color=color, 
                thickness=-1)
        return img


    def create_triangle(self, background=(255, 255, 255)):

        img = self.create_canvas(background)

        p1  = (np.random.randint(-self.max_object, self.max_object), 
                        np.random.randint(-self.max_object, self.max_object))
        p2  = (np.random.randint(-self.max_object, self.max_object), 
                        np.random.randint(-self.max_object, self.max_object))
        p3  = (np.random.randint(-self.max_object, self.max_object), 
                        np.random.randint(-self.max_object, self.max_object))
        

        # translate points to center
        p1 = (p1[0] + self.height//2, p1[1] + self.width//2)
        p2 = (p2[0] + self.height//2, p2[1] + self.width//2)
        p3 = (p3[0] + self.height//2, p3[1] + self.width//2)


        triangle_contour = np.array([p1, p2, p3])
        color = tuple(np.random.randint(0, 255, 3))

        cv2.drawContours(img, [triangle_contour], 0, color, -1)
        return img


    def create_hex(self, background=(255, 255, 255)):

        img = self.create_canvas(background)
        side = 6
        sizex = np.random.randint(0, self.max_object)
        sizey = np.random.randint(0, self.max_object)
        points = [ ((math.cos(th) + 1) * sizex, (math.sin(th) + 1) * sizey)
            for th in [i * (2 * math.pi) / side for i in range(side)]
            ]  
  
        contour = np.array(points)
        color = tuple(np.random.randint(0, 255, 3))

        cv2.drawContours(img, [contour], 0, color, -1)
        return img


    def create_circle(self, background=(255, 255, 255)):
        img = self.create_canvas(background)

        radius = np.random.randint(0, self.max_object)
        center = (self.height//2, self.width//2)
        color = tuple(np.random.randint(0, 255, 3))
        cv2.circle(img, center, radius, color, -1)
        return img


    def create_capsule(self, background=(255, 255, 255)):

        img = self.create_canvas(background)

        img = np.uint8(np.ones((self.height, self.width, 3)))
        object_height = np.random.randint(0, self.max_object)
        object_width = np.random.randint(0, self.max_object)

        start_point = (self.width//2 - object_width//2, self.height//2 - object_height//2)
        end_point = (self.width//2 + object_width//2, self.height//2 + object_height//2)
        color = tuple(np.random.randint(0, 255, 3))
        img = cv2.rectangle(img, 
                pt1=start_point, 
                pt2=end_point, 
                color=color, 
                thickness=-1)

        radius = object_width//2
        center = (start_point[0] + object_width//2, start_point[1])
        cv2.circle(img, center, radius, color, -1)

        center = (end_point[0] - object_width//2, end_point[1])
        cv2.circle(img, center, radius, color, -1)
        return img


    def create_ellipse(self, background=(255, 255, 255)):

        img = self.create_canvas(background)

        major_axis = np.random.randint(0, self.max_object)
        minor_axis = np.random.randint(0, self.max_object)

        center = (self.height//2, self.width//2)
        axesLength = (major_axis, minor_axis)
        
        angle = np.random.uniform(-np.pi, np.pi)
        color = tuple(np.random.randint(0, 255, 3))

        cv2.ellipse(img, 
                    center, 
                    axesLength,
                    angle,
                    color=color, 
                    thickness=-1)
        return img 


    def sample(self, n = 100, type='circle', background=(255, 255, 255)):
        if not (type in self.objects.keys()): 
            raise ValueError('Unkown type found, allowed types: ', self.objects.keys())

        objects = [self.objects[type] for _ in range(n)]
        objects = self.transform(images = objects)
        return objects