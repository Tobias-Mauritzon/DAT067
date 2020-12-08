import cv2
from DistanceEstimator import DistanceEstimator

# Author: Philip
# Reviewed by: 
# Date: 2020-12-05

# Author: Joachim Antfolk
# Reviewed by: 
# Date: 2020-12-08

"""This class loads a specific cascade classifier and uses it to find an object with the function findObject"""
class HaarCascade_Model():
	def __init__(self, objectName):
		self.objectName = objectName	# saves the name of the object
		self.__loadClassifier()   # loads the specific classifier for the object
		self.__setColors()
		# default values
		self.scaleFactor_def = 1.05 # how much the image size is reduced at each image scale
		self.scaleFactor_0 = self.scaleFactor_def
		self.scaleFactor_1 = self.scaleFactor_def
		self.minNeighbors_def = 5 # how many neighbors each candidate rectangle should have to retain it, higher less detections but higher quality
		self.minNeighbors_0 = self.minNeighbors_def
		self.minNeighbors_1 = self.minNeighbors_def
		self.minSize_def = 0 # the minimum possible object size, objects smaller thant this are ignored
		self.minSize_0 = self.minSize_def
		self.minSize_1 = self.minSize_def

        # sets width of obejct to measure distance to. //1.8 for car //0.52 for num.plate //0.15 for face
		self.regEstimator = DistanceEstimator(0.52)
		self.carEstimator = DistanceEstimator(1.8)

		# detect plates boolean
		self.detectPlates = False

	# Loads the classifier for the object
	def __loadClassifier(self):
		if self.objectName == "Car":
			self.carCascade = cv2.CascadeClassifier('cascades/haarcascade_cars.xml')
			self.plateCascade = cv2.CascadeClassifier('cascades/haarcascade_russian_plate_number.xml')
		elif self.objectName =="OTHER":
			pass
		
	def __setColors(self):
		if self.objectName == "Car":
			self.carBorderColor = (255,0,0)
			self.carFontColor = (11,255,255)
			self.plateBorderColor = (0,255,0)
			self.plateFontColor = (255,11,255)
		elif self.objectName == "OTHER":
			pass


	def findCars(self,image):
		#Convert to gray
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cars = self.carCascade.detectMultiScale3(gray, scaleFactor=self.scaleFactor_0, minNeighbors=self.minNeighbors_0, minSize=(self.minSize_0,self.minSize_0),outputRejectLevels = True)
		i = 0
		for(x, y, w, h) in cars[0]:
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h

            #Calculate distance to car
			distance = self.carEstimator.estimate_distance(w)

			#Draws the rectangle around the object
			objectRectangle = cv2.rectangle(image, (x, y), (end_cord_x, end_cord_y), self.carBorderColor, stroke)
			cv2.rectangle(image, (x, end_cord_y), (end_cord_x, end_cord_y + 40), self.carBorderColor, -1)

			# set the text font for the label
			font = cv2.FONT_HERSHEY_SIMPLEX
			#Display the text
			carWeights = cars[2]
			cv2.putText(objectRectangle,self.objectName + " " + str(round(carWeights[i][0],2)),(x, y-10), font, 0.5, self.carFontColor, 2, cv2.LINE_AA)
			i+=1
			if self.detectPlates:
				plates = self.plateCascade.detectMultiScale3(gray, scaleFactor=self.scaleFactor_1, minNeighbors=self.minNeighbors_1, minSize=(self.minSize_1,self.minSize_1),outputRejectLevels = True)
				j=0
				for(px,py,pw,ph) in plates[0]:
					end_cord_px = px + pw
					end_cord_py = py + ph

                    #Calculate distance to registration plate
					tempDistance = self.regEstimator.estimate_distance(pw)
					if(tempDistance < distance): #Use the closest value to car
					    distance = tempDistance

					#Draws the rectangle around the object
					objectRectangle = cv2.rectangle(image, (px, py), (end_cord_px, end_cord_py), self.plateBorderColor, stroke)
					#Display the text
					plateWeights = plates[2]
					cv2.putText(objectRectangle,"Licence Plate" + " " + str(round(plateWeights[j][0],2)),(px, py-10), font, 0.5, self.plateFontColor, 2, cv2.LINE_AA)
					j+=1

            #Display the distance
			cv2.putText(image, distance, (x + 10, end_cord_y + 30), font, 0.7, self.carFontColor)

            

	"""
	# Finds where the object is and draws a rectangle and a label
	def findObject(self,image):
		#Convert to gray
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		objects = self.myCascade.detectMultiScale3(gray, scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors, minSize=(self.minSize,self.minSize),outputRejectLevels = True)
		i = 0
		for(x, y, w, h) in objects[0]:
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h
			#Draws the rectangle around the object
			objectRectangle = cv2.rectangle(image, (x, y), (end_cord_x, end_cord_y), self.borderColor, stroke)
			# set the text font for the label
			font = cv2.FONT_HERSHEY_SIMPLEX
			#Display the text
			weights = objects[2]
			cv2.putText(objectRectangle,self.objectName + " " + str(round(weights[i][0],2)),(x, y-10), font, 0.5, self.fontColor, 2, cv2.LINE_AA)
			i+=1
	"""
	def setDetectPlates(self):
		if self.detectPlates:
			self.detectPlates = False
		else:
			self.detectPlates = True

	# sets the scaleFactor
	def setScaleFactor(self, factor, index):
		if index == 0:
			self.scaleFactor_0 = factor
		elif index == 1:
			self.scaleFactor_1 = factor

	
	# sets the minNeghbors
	def setMinNeighbors(self, number, index):
		if index == 0:
			self.minNeighbors_0 = number
		elif index == 1:
			self.minNeighbors_1 = number

	# sets the min size
	def setMinsize(self, number, index):
		if index == 0:
			self.minSize_0 = number
		elif index == 1:
			self.minSize_1 = number
	
	# resets all values to default
	def resetValues(self,index):
		if index == 0:
			self.scaleFactor_0 = self.scaleFactor_def
			self.minNeighbors_0 = self.minNeighbors_def
			self.minSize_0 = self.minSize_def
		elif index == 1:
			self.scaleFactor_1 = self.scaleFactor_def
			self.minNeighbors_1 = self.minNeighbors_def
			self.minSize_1 = self.minSize_def

	