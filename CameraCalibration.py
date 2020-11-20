"""
#Author: Joachim Antfolk
#Reviewed by:
#Date: 2020-11-19
"""

class CameraCalibration:
    """
    This class handles the calibration of the camera. 
    It also handles reading and saving this information in a .ini file
    """

    def __init__(self, width: int, height: int, distance: float):
        """
        Initiates CameraCalibration object with real dimension integer references 'width' and 'height' 
        """
        self.width = width
        self.height = height
        self.distance = distance

    def write_to_file(self, fx: int, fy: int):
        """
        Writes the integer parameters fx and fy to camera_info.ini  
        otherwise throws exception 
        """
        try:
            file = open("camera_info.ini", "w")
            file.write("fx:" + str(fx) + "\nfy:" + str(fy))
        except Exception:
            raise Exception("Could not write to file!")
        finally:
            file.close()
        
    def read_from_file(self) -> (int, int):
        """ 
        Reads the relevant camera inforamtion from camera_info.ini 
        returns a tuple in the format (fx, fy) 
        otherwise throws exception 
        """
        try:
            file = open("camera_info.ini", "r")
            fx = int(file.readline().split(":")[1])
            fy = int(file.readline().split(":")[1])
            retval = (fx, fy)
        except Exception:
            raise Exception("Could not read from file!")
        finally:
            file.close()
            return retval
        
    def calibrate(self, img_width: int, img_height: int) -> (int, int):
        """
        Takes the width and height of the recognised object in pixels 
        and calculates the focal length using the formula: 
        Focal length = (Size in image x Distance) / Real size
        """
        fx = (img_width * self.distance) / self.width
        fy = (img_height * self.distance) / self.height
        try:
            self.write_to_file(fx, fy)
        except Exception:
            raise Exception("Could not write to file!")
        return (fx, fy)