"""
#Author: Joachim Antfolk, William Jönsson
#Reviewed by: Tobias Mauritzon
#Reviewed on: 2020-12-04
"""

"""
#Author: Joachim Antfolk
#Reviewed by: 
#Reviewed on: 2020-12-15
"""

from cv2 import cv2
import numpy as numpy
from typing import Tuple
from typing import List

class DistanceEstimator:
    """
    This class handles estimating the distance to an object in an image.
    """

    def __init__(self, real_size: float):
        """
        Initiates DistanceEstimator object with focal length data and the real dimension of object. 
        """
        self.real_size = real_size

        try:
            self.focal = self.__read_from_file()[1]
        except Exception:
            self.focal = 500 #Placeholder

    def estimate_distance(self, dimension: int) -> str:
        """
        Estimates the distance to every object in the rectangle list 'objects' by 
        using the specified dimension ("h" for height or "w" for width) and draws this on the image 'img'
        """
        return self.__calculate(dimension)

    def __read_from_file(self) -> (float, float):
        """ 
        Reads the relevant camera inforamtion from camera_info.ini 
        returns a tuple in the format (fx, fy) 
        otherwise throws exception 
        """
        try:
            file = open("camera_info.ini", "r")
            fx = float(file.readline().split(":")[1])
            fy = float(file.readline().split(":")[1])
            retval = (fx, fy)
        except Exception:
            raise Exception("Could not read from file!")
        finally:
            file.close()
            return retval

    def __calculate(self, dimension: int) -> str:
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
