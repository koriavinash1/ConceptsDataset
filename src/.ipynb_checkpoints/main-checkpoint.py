import cv2
import os
import numpy as np
import matplotlib.pyplot as plt 
from src.utils import CreateObject


class CreateDataset(object):
    def __init__(self, 
                    N= 10000, 
                    batch_size=32,
                    height=128,
                    width=128,
                    Kconcepts=5, 
                    nclasses=3,
                    classes={1: ['circe', 'capsule', 'ellipse'],
                                2: ['square', 'pentagon', 'triangle']},
                    save_dir='../../data'):
        self.Ndatapoints = N
        self.batch_size = batch_size
        self.Kconcepts=Kconcepts
        self.class_rules = classes
        self.height = height
        self.width = width
        self.save_dir = save_dir

        os.makedirs(self.save_dir, exist_ok=True)
        for i in range(nclasses):
            os.makedirs(os.path.join(self.save_dir, f'class-{i}'), exist_ok=True)

        self.object_creator = CreateObject(self.height, self.width)

    def sample_objects(self):
        classes = {}
        nclassobjects = np.random.randint(2, self.Kconcepts)
        classes[0] = list(np.random.choice(self.class_rules[1], size=nclassobjects)) + \
                        list(np.random.choice(self.class_rules[2], size=self.Kconcepts - nclassobjects))

        classes[1] = list(np.random.choice(self.class_rules[1], size=self.Kconcepts))
        classes[2] = list(np.random.choice(self.class_rules[2], size=self.Kconcepts))
        return classes

    def save_images(self, images, class_, start_idx=0):
        path = os.path.join(self.save_dir, f'class-{class_}')
        for i, img in enumerate(images):
            idx = i + (start_idx)*self.batch_size*(class_+1)
            cv2.imwrite(os.path.join(path, f'{idx}.png'), img)
        pass


    def create(self):
        for ibatch in range(self.Ndatapoints//self.batch_size):
            background = tuple([int(a) for a in np.random.randint(0, 50, 3)])
            classes = self.sample_objects()

            for key, concepts in classes.items():
                objects = [self.object_creator.sample(n=self.batch_size, 
                                                        type=type_) for type_ in concepts]
                images = self.object_creator.combine(objects, background=background)
                self.save_images(images, key, ibatch)
