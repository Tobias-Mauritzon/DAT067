"""
#Author: Joachim Antfolk
#Reviewed by: William Jönsson
#Date: 2020-11-20
"""

import numpy as np
import cv2

class CameraCalibration:
    """
    This class handles the calibration of the camera. 
    It also handles reading and saving this information in a .ini file
    """

    def __init__(self, width: float, height: float, distance: float):
        """
        Initiates CameraCalibration object with real dimension float references 'width', 'height' and distance in meters
        """
        self.width = width
        self.height = height
        self.distance = distance

    def calibrateCamera(self, patternSquareSize: int):
        """
        Calibrates camera using webcam feed with a checkerboard pattern.
        Parameters:
            patternSquareSize - checkerboard square size in mm
        """
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((7*6,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        objp = objp * patternSquareSize

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(3, 640)
        cap.set(4, 480)

        # Counter to keep track of calibration images taken - needs REQUIRED_IMAGE_AMOUNT to calibrate
        imageCounter = 0
        REQUIRED_IMAGE_AMOUNT = 5

        print("Press space to use current image to calibrate. Need ", REQUIRED_IMAGE_AMOUNT - imageCounter, " more images.")

        while True:
            success, img = cap.read()
    
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            cv2.imshow('CalibrationVideo',cv2.flip(img, 2))

            # Press space to use image for calibration
            if cv2.waitKey(1) & 0xFF == ord(' '):
                # Find the chess board corners
                ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

                # If found, add object points, image points (after refining them)
                if ret == True:
                    imageCounter += 1
                    objpoints.append(objp)

                    cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                    imgpoints.append(corners)

                    # Draw and display the corners
                    cv2.drawChessboardCorners(img, (7,6), corners,ret)
                    cv2.imshow('CalibrationImage',cv2.flip(img, 2))
                    print("Press space to use current image to calibrate. Need ", REQUIRED_IMAGE_AMOUNT - imageCounter, " more images.")

                if imageCounter >= requiredImageAmount:
                    break

        print("Calculating camera matrix etc...")
        ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        print("...done calculating.")

        cv2.destroyAllWindows()
        self.cameraMatrix = cameraMatrix

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