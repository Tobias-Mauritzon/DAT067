import cv2

# Author: Philip
# Reviewed by: 
# Date: 2020-12-05

"""This class loads a specific cascade classifier and uses it to find an object with the function findObject"""
class HaarCascade_Model():
	def __init__(self, objectName):
		self.objectName = objectName	# saves the name of the object
		self.__loadClassifier()   # loads the specific classifier for the object
		# default values
		self.scaleFactor = 1.1 # how much the image size is reduced at each image scale
		self.scaleFactor_def = self.scaleFactor
		self.minNeighbors = 5 # how many neighbors each candidate rectangle should have to retain it, higher less detections but higher quality
		self.minNeighbors_def = self.minNeighbors
		self.minSize = 0 # the minimum possible object size, objects smaller thant this are ignored
		self.minSize_def = self.minSize

	# Loads the classifier for the object
	def __loadClassifier(self):
		if self.objectName == "Cars":
			self.myCascade = cv2.CascadeClassifier('cascades/haarcascade_cars.xml')
		elif self.objectName =="SOMEOBJECT":
			pass #insert other classifiers here

	# Finds where the object is and draws a rectangle and a label
	def findObject(self,image):
		#Convert to gray
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		objects = self.myCascade.detectMultiScale(gray, scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors, minSize=(self.minSize,self.minSize))
		for(x, y, w, h) in objects:
			color = (255,0,0)
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h
			#Draws the rectangle around the object
			objectRectangle = cv2.rectangle(image, (x, y), (end_cord_x, end_cord_y), color, stroke)
			# set the text font for the label
			font = cv2.FONT_HERSHEY_SIMPLEX
			#Display the text
			cv2.putText(objectRectangle,"CAR",(x, y-10), font, 0.5, (11,255,255), 2, cv2.LINE_AA)
	
	# sets the scaleFactor
	def setScaleFactor(self, factor):
		self.scaleFactor = factor
	
	# sets the minNeghbors
	def setMinNeighbors(self, number):
		self.minNeighbors = number

	# sets the min size
	def setMinsize(self, number):
		self.minSize = number
	
	# resets all values to default
	def resetValues(self):
		self.scaleFactor = self.scaleFactor_def
		self.minNeighbors = self.minNeighbors_def
		self.minSize = self.minSize_def

	