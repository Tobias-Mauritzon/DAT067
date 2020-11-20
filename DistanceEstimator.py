"""
#Author: Joachim Antfolk
#Reviewed by:
#Date: 2020-11-19
"""

from cv2 import cv2 
import numpy as numpy
from typing import Tuple
from typing import List

class DistanceEstimator:
    """
    This class handles estimating the distance to an object from an image.
    """

    def __init__(self, focal: int, real_size: float):
        """
        Initiates DistanceEstimator object with focal length data and the real dimension of object. 
        """
        self.focal = focal
        self.real_size = real_size

    #def estimate(self, img: numpy.array, objects: List[Tuple[int, int, int, int]], dimension: str):
    def estimate_distance(self, img: numpy.ndarray, objects: List, dimension: str):
        """
        Estimates the distance to every object in the rectangle list 'objects' by 
        using the specified dimension ("h" for height or "w" for width) and draws this on the image 'img'
        """
        for(x, y, w, h) in objects:
            if dimension == "h":
                distance = self.calculate(h)
            elif dimension == "w":
                distance = self.calculate(w)
            else:
                distance = "Invalid"

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
            cv2.rectangle(img, (x, y+h), (x+w, y+h+40), (255, 0, 255), -1)
            cv2.putText(img, distance, (x + 10, y + h + 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255))

    def calculate(self, dimension: int) -> str:
        """
        Calculates the distance and returns it as a string of the 
        distance in meters rounded to three places
        """
        return str(round((self.real_size*self.focal)/dimension, 1)) + " m"

    def update_focal(self, new_focal: int):
        """
        Updates the distance estimators focal length attribute
        """
        self.focal = new_focal

    def update_size(self, new_size: float):
        """
        Updates the distance estimators real size attribute
        """
        self.real_size = new_size
    