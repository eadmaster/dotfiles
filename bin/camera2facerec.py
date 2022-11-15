#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: merge with bin/camera2facerec.py.bad


import logging
import os
import re
import face_recognition.api as face_recognition
import multiprocessing
import itertools
import sys
import PIL.Image
import numpy as np
import cv2
import math
import time
import argparse

PROGRAM_NAME = os.path.basename(sys.argv[0])


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 1:
            logging.warning("More than one face found in {}. Only considering the first face.".format(file))

        if len(encodings) == 0:
            logging.warning("No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])
        break

    return known_names, known_face_encodings



def getFaceBox(net, frame,conf_threshold = 0.75):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn,1.0,(300,300),[104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > conf_threshold:
            x1 = int(detections[0,0,i,3]* frameWidth)
            y1 = int(detections[0,0,i,4]* frameHeight)
            x2 = int(detections[0,0,i,5]* frameWidth)
            y2 = int(detections[0,0,i,6]* frameHeight)
            bboxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn,(x1,y1),(x2,y2),(0,255,0),int(round(frameHeight/150)),8)

    return frameOpencvDnn , bboxes


#TODO: replace /home/andy/caffe  CAFFE_ROOT
faceProto = "/home/andy/caffe/opencv_face_detector.pbtxt"
faceModel = "/home/andy/caffe/opencv_face_detector_uint8.pb"

ageProto = "/home/andy/caffe/age_deploy.prototxt"
ageModel = "/home/andy/caffe/age_net.caffemodel"

genderProto = "/home/andy/caffe/gender_deploy.prototxt"
genderModel = "/home/andy/caffe/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100']
genderList = ['male', 'female']

#load the network
ageNet = cv2.dnn.readNet(ageModel,ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
faceNet = cv2.dnn.readNet(faceModel, faceProto)

known_people_folder = "/home/andy/pendrive/Documents/img/id/faces_cropped"
known_face_names, known_face_encodings = scan_known_people(known_people_folder)

cap = cv2.VideoCapture(0)
padding = 20

prev_faces_count = 0
new_face_appeared_ts = 0
name = ""
gender = ""
age = ""

while cv2.waitKey(1) < 0:
	#read frame
	#t = time.time()
	hasFrame , frame = cap.read()

	if not hasFrame:
		cv2.waitKey()
		break
	#creating a smaller frame for better optimization
	small_frame = cv2.resize(frame,(0,0),fx = 0.5,fy = 0.5)

	frameFace, bboxes = getFaceBox(faceNet, small_frame)
	#print("bboxes:" + str(bboxes))
	
	#if len(bboxes) == prev_faces_count:
	#	# no new face
	#	continue
	# else
	# TODO: grab multiple pic of the same face, try to recognize
	#new_face_appeared_ts = ...
	
	# alt. with dlib
	rgb_small_frame = small_frame[:, :, ::-1]   # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	face_locations = face_recognition.face_locations(rgb_small_frame)
	face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
	#print("face_locations:" + str(face_locations))

	if (name or gender) and len(face_locations) == prev_faces_count:
		#cv2.imshow(PROGRAM_NAME, frameFace)
		# no new face
		continue
	
	prev_faces_count = len(face_locations)
	#print(prev_faces_count)
	#print(len(bboxes))
	
	for bbox in bboxes:
		face = small_frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),
				max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
		
		# try to detect the person
		#face_locations = [ tuple(bbox) ]
		if face_encodings:
			face_encoding = face_encodings[0]
			# find the known face with the smallest distance to the new face
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]
				print("recognized: " + name)
				cv2.putText(frameFace, name, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
		else:
			name = ""
			# if it fails, detect gender and age
			blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
			genderNet.setInput(blob)
			genderPreds = genderNet.forward()
			gender = genderList[genderPreds[0].argmax()]
			#print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

			ageNet.setInput(blob)
			agePreds = ageNet.forward()
			age = ageList[agePreds[0].argmax()]
			#print("Age Output : {}".format(agePreds))
			#print("Age : {}, conf = {:.3f}".format(age, agePreds[0].max()))
			print("detected face of a " + gender + ", age " + age)
			label = "{},{}".format(gender, age)
			cv2.putText(frameFace, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
		# end if
	# end for bboxes
	
	if len(face_locations):
		cv2.imshow(PROGRAM_NAME, frameFace)
	
	#print("time : {:.3f}".format(time.time() - t))


   
        