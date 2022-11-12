import cv2
from imgaug import augmenters as iaa
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import math

class CreateObject(object):
    def __init__(self, height, width):
        self.height = height 
        self.width = width
        self.min_object = self.height//10
        self.max_object = self.height//4
        self.transform = iaa.Sequential([
                            iaa.Affine(rotate=(-90, 90),
                                        translate_percent=(-0.28, 0.28),
                                        shear=(-25, 25),
                                        mode='symmetric'),
                            iaa.AdditiveGaussianNoise(scale=(1, 1)),
                        ]) 


        self.objects = {'circle': self.create_circle,
                        'square': self.create_square,
                        'hexagon': self.create_polygon(6),
                        'pentagon': self.create_polygon(5),
                        'octagon': self.create_polygon(8),
                        'ellipse': self.create_ellipse,
                        'capsule': self.create_capsule,
                        'triangle': self.create_polygon(3)}


    def create_canvas(self, background=(0, 0, 0)):
        img = np.uint8(np.zeros((self.height, self.width, 3)))
        img[:,:, 0] = background[0]
        img[:,:, 1] = background[1]
        img[:,:, 2] = background[2]
        return img 


    def create_square(self, background=(255, 255, 255)):
        img = self.create_canvas()
        object_height = np.random.randint(self.min_object, self.max_object)
        object_width = np.random.randint(self.min_object, self.max_object)

        start_point = (int(self.width//2 - object_width//2), int(self.height//2 - object_height//2))
        end_point = (int(self.width//2 + object_width//2), int(self.height//2 + object_height//2))
        color = tuple([int(a) for a in np.random.randint(0, 255, 3)])

        img = cv2.rectangle(img, 
                start_point, 
                end_point, 
                color, 
                thickness=-1)
        return img


    def create_triangle(self, background=(255, 255, 255)):

        img = self.create_canvas()

        p1  = (np.random.randint(-self.max_object, self.max_object), 
                        np.random.randint(-self.max_object, self.max_object))
        p2  = (np.random.randint(-self.max_object, self.max_object), 
                        np.random.randint(-self.max_object, self.max_object))
        p3  = (np.random.randint(-self.max_object, self.max_object), 
                        np.random.randint(-self.max_object, self.max_object))
        

        # translate points to center
        p1 = (int(p1[0] + self.height//2), int(p1[1] + self.width//2))
        p2 = (int(p2[0] + self.height//2), int(p2[1] + self.width//2))
        p3 = (int(p3[0] + self.height//2), int(p3[1] + self.width//2))


        triangle_contour = np.array([p1, p2, p3])
        color = tuple([int(a) for a in np.random.randint(0, 255, 3)])

        cv2.drawContours(img, [triangle_contour], 0, color, -1)
        return img


    def create_polygon(self, side=6):
        def create_object(background=(255, 255, 255)):
            img = self.create_canvas()
            sizex = np.random.randint(self.min_object, self.max_object)
            sizey = np.random.randint(self.min_object, self.max_object)
            points = [ (int((math.cos(th) + 1) * sizex), int((math.sin(th) + 1) * sizey))
                for th in [i * (2 * math.pi) / side for i in range(side)]
                ]  

            contour = np.array(points)
            contour[:, 0] += int(self.width//2 - self.max_object//2)
            contour[:, 1] += int(self.height//2 - self.max_object//2)
            color = tuple([int(a) for a in np.random.randint(0, 255, 3)])

            cv2.drawContours(img, [contour], 0, color, -1)
            return img
        return create_object


    def create_circle(self, background=(255, 255, 255)):
        img = self.create_canvas()

        radius = int(np.random.randint(self.min_object, self.max_object))
        center = (int(self.height//2), int(self.width//2))
        color = tuple([int(a) for a in np.random.randint(0, 255, 3)])
        cv2.circle(img, center, radius, color, -1)
        return img


    def create_capsule(self, background=(255, 255, 255)):

        img = self.create_canvas()

        object_height = np.random.randint(2*self.min_object, self.max_object)
        object_width = np.random.randint(self.min_object, self.max_object)

        start_point = (int(self.width//2 - object_width//2), int(self.height//2 - object_height//2))
        end_point = (int(self.width//2 + object_width//2), int(self.height//2 + object_height//2))
        color = tuple([int(a) for a in np.random.randint(0, 255, 3)])
        img = cv2.rectangle(img, 
                pt1=start_point, 
                pt2=end_point, 
                color=color, 
                thickness=-1)

        radius = int(object_width//2)
        center = (int(start_point[0] + object_width//2), int(start_point[1]))
        cv2.circle(img, center, radius, color, -1)

        center = (int(end_point[0] - object_width//2), int(end_point[1]))
        cv2.circle(img, center, radius, color, -1)
        return img


    def create_ellipse(self, background=(255, 255, 255)):

        img = self.create_canvas()

        major_axis = int(np.random.randint(2*self.min_object, self.max_object))
        minor_axis = int(np.random.randint(self.min_object, self.max_object))

        center = (int(self.height//2), int(self.width//2))
        axesLength = (major_axis, minor_axis)
        
        angle = int(np.random.uniform(0, 360))
        color = tuple([int(a) for a in np.random.randint(0, 255, 3)])

        cv2.ellipse(img, 
                    center, 
                    axesLength,
                    angle,
                    0,
                    360,
                    color, 
                    -1)
        return img 


    def sample(self, n = 100, type='circle'):
        if not (type in self.objects.keys()): 
            raise ValueError('Unkown type found, allowed types: ', self.objects.keys())

        objects = [self.objects[type]() for _ in range(n)]
        objects = self.transform(images = objects)
        return np.array(objects)

    def combine(self, concepts,  background=(255, 255, 255)):
        data = np.zeros_like(concepts[0])*1.0
        data[..., 0] =  background[0]
        data[..., 1] =  background[1]
        data[..., 2] =  background[2]
        N = len(concepts)
        for iconcept in concepts:
            data += iconcept*1.0/N

        # data = np.clip(data, 0, 255)
        # data = 255*(data - np.min(data))/(np.max(data) - np.min(data))
        data = np.uint8(data)
        return data 



def show_image(images, 
                title=('original img', 'recon img', 'intervened img'),
                transpose = False):
    
    img_size = 3
    nrows = len(images)
    ncols = len(images[0])

    if transpose:
        ncols = len(images)
        nrows = len(images[0])
                

    nimgs = nrows*ncols
    
    plt.clf()
    fig = plt.figure(num = nimgs, figsize=(img_size*ncols, img_size*nrows))
    fig.tight_layout()
    gs = gridspec.GridSpec(nrows, ncols)
    gs.update(wspace=0.2, hspace=0.1)

    for ilist, img_set in enumerate(images):

        for iset, img in enumerate(img_set):
            xidx = ilist; yidx = iset 
            if transpose:
                yidx = ilist; xidx = iset

            ax = plt.subplot(gs[xidx, yidx])
            ax.imshow(img)

                
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_aspect('equal')
            ax.set_title('$'+title[ilist]+'$')
            ax.tick_params(bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off' )


        
    plt.tight_layout()
    plt.savefig('test.png')
    plt.show()