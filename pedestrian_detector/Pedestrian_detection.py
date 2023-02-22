from re import T
import numpy as np
import cv2
import os
import imutils
import shutil

# Código
# https://data-flair.training/blogs/pedestrian-detection-python-opencv/

NMS_THRESHOLD=0.3
MIN_CONFIDENCE=0.2
#Porcentaje de error es: 5.096430036930652
# modificar threshold y confidencia utilizando market originales
#Porcentaje de error es: 11.908083709478868
# NMS_THRESHOLD=0.1
# MIN_CONFIDENCE=0.8



def pedestrian_detection(image, model, layer_name, personidz=0):
	(H, W) = image.shape[:2]
	results = []


	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	model.setInput(blob)
	layerOutputs = model.forward(layer_name)

	boxes = []
	centroids = []
	confidences = []

	for output in layerOutputs:
		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if classID == personidz and confidence > MIN_CONFIDENCE:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))
	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idzs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)
	# ensure at least one detection exists
	if len(idzs) > 0:
		# loop over the indexes we are keeping
		for i in idzs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			# update our results list to consist of the person
			# prediction probability, bounding box coordinates,
			# and the centroid
			res = (confidences[i], (x, y, x + w, y + h), centroids[i])
			results.append(res)
	# return the list of results
	return results

# ******************************************************************************************
img_market = "0002_c1s1_000551_01.jpg" #argv[1]
img_stylegan = "1_1001_00000.jpg"
path_market = "/home/laura/Escritorio/stylegan3/_noviembre22_resize/" 
#"/home/laura/Escritorio/stylegan3/_screenshots/NuevasStyleganCharm10052022/content/images/"
#"/home/laura/Escritorio/stylegan3/_screenshots/Market1501_train/train/"
path_stylegan = "/home/laura/Escritorio/stylegan3/_screenshots/432IMGsJunio22_resize/"
path_descartadas = "/home/laura/Escritorio/stylegan3/_noviembre22_resize_descartadas/" 
"/home/laura/Escritorio/stylegan3/_screenshots/NuevasStyleganCharm10052022/content/descartadas/"
#"/home/laura/Escritorio/stylegan3/_screenshots/432IMGsJunio22_resize_descartadas/"
es_market = True
if (es_market):
	data_dir = path_market
else :
	data_dir = path_stylegan

#test_img = cv2.imread(path_market + img_market)
# ******************************************************************************************



labelsPath = "/home/laura/Escritorio/stylegan3/_screenshots/editor_imgs/pedestrian_detector/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

weights_path = "/home/laura/Escritorio/stylegan3/_screenshots/editor_imgs/pedestrian_detector/yolov4-tiny.weights"
config_path = "/home/laura/Escritorio/stylegan3/_screenshots/editor_imgs/pedestrian_detector/yolov4-tiny.cfg"

model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
'''
model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
'''
layer_name = model.getLayerNames()
#layer_name = model.getUnconnectedOutLayersNames()

for i in model.getUnconnectedOutLayers():
	tralara = layer_name[i[0] - 1] 

layer_name = [layer_name[i[0] - 1] for i in model.getUnconnectedOutLayers()]
#layer_name = model.getUnconnectedOutLayersNames()
#layer_name = [layer_name[i[0] - 1] for i in model.getUnconnectedOutLayers()]

#layer_name = model.getLayerNames()
#layer_name = [layer_name[i[0] - 1] for i in model.getUnconnectedOutLayers()]
#cap = cv2.VideoCapture("streetup.mp4")
writer = None

contador_imgs = 0
contador_errores = 0

CONFIANZA_BASE = 0.6 # para testing market 0.5
UMBRAL_CONFIANZA = 1 # para testing market 6
print ("Carpeta: " + path_market)
for i in range(UMBRAL_CONFIANZA):

	MIN_CONFIDENCE= CONFIANZA_BASE # + (i*0.1)

	#for j in range(6):
	# el NMS_THRESHOLD es el umbral para rellenar los cuadrados de multiples apariencias
	#	NMS_THRESHOLD=0 + (j*0.3)
	#	print ("Calculando..... MIN_CONFIDENCE: " + "{:.2f}".format(MIN_CONFIDENCE)  + " NMS_THRESHOLD %: " + "{:.2f}".format(NMS_THRESHOLD))

	contador_errores = 0
	contador_imgs = 0
	contador_personas = 0
	for folder2 in os.listdir(data_dir):
		contador_personas = contador_personas + 1
		#print (contador_personas)
		folder_path = os.path.join(data_dir, folder2)
		for file in os.listdir(folder_path):

			img_path = os.path.join(folder_path+ "/", file)
			data_img = cv2.imread(img_path)


			# agregamos un borde a la imagen
			color = [101, 52, 152] # 'cause purple!
			# border widths; I set them all to 150
			top, bottom, left, right = [150]*4
			data_img = cv2.copyMakeBorder(data_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
			#cv2.imwrite("/home/laura/Escritorio/stylegan3/_screenshots/432IMGsJunio22_resize_descartadas/prueba.jpg", data_img)

		#	data_img = imutils.resize(data_img, width=700)
			results = pedestrian_detection(data_img, model, layer_name,
				personidz=LABELS.index("person"))

			# dibuja el rectángulo en el peatón
			#for res in results:
			#	cv2.rectangle(data_img, (res[1][0],res[1][1]), (res[1][2],res[1][3]), (0, 255, 0), 2)

			if (len(results) == 0):
				contador_errores = contador_errores + 1
				#print ("No se detectó: " + file)
				# movemos la imagen a la carpeta de descartadas 
				if (es_market):

					new_path = path_descartadas + folder2 + "_Pedestrian"
					if not (os.path.isdir(new_path)): os.mkdir(new_path)
					shutil.move(img_path, new_path)

			# muestra la imagen del peatón marcado
			#cv2.imshow("Detection",data_img)
			contador_imgs = contador_imgs + 1
			

			#key = cv2.waitKey(1)
			#if key == 27:
			#	break
	porcentaje = (contador_errores * 100) / contador_imgs 
	print ("NMS_THRESHOLD: " + "{:.2f}".format(NMS_THRESHOLD)  + " " + "MIN_CONFIDENCE: " + "{:.2f}".format(MIN_CONFIDENCE)  + "Error %: " + str(porcentaje))
	print ("MIN_CONFIDENCE: " + "{:.2f}".format(MIN_CONFIDENCE)  + " Error %: " + str(porcentaje))
	print ("Contador errores : " + str(contador_errores)  + " Contador imagenes %: " + str(contador_imgs))

# filtrado en las generadas por stylegan3 editing charm
# contador_errores = 2882
# contador_imgs = 17690

#cap.release()
#print ("Porcentaje de error es: " + str(porcentaje))
cv2.destroyAllWindows()


# ************************************* RESULTADOS ************************************************
#MIN_CONFIDENCE: 0.50 Error %: 5.096430036930652
#MIN_CONFIDENCE: 0.60 Error %: 6.4587607714402955
#MIN_CONFIDENCE: 0.70 Error %: 8.461222814936397
#MIN_CONFIDENCE: 0.80 Error %: 11.908083709478868
#MIN_CONFIDENCE: 0.90 Error %: 19.630693475584735
#MIN_CONFIDENCE: 1.00 Error %: 100.0


# CON STYLEGAN
# 16830 imágenes # filtradas 2755
# MIN_CONFIDENCE: 0.70 Error %: 16.369578134284016

# Stylegan3 Junio 2022
# NMS_THRESHOLD: 0.30 MIN_CONFIDENCE: 0.60Error %: 9.121787929506745
# MIN_CONFIDENCE: 0.60 Error %: 9.121787929506745
# NMS_THRESHOLD: 0.30 MIN_CONFIDENCE: 0.20Error %: 6.756632699899018
# MIN_CONFIDENCE: 0.20 Error %: 6.756632699899018

#44548 - Se descartaron 2673
#41875 - Se descartaron 3819
#TOTAL = 			   6492 imágenes descardas en total

# despues de quitar 50 quedó así Stylegan3 17 - junio - 22
# 22.455 imágenes se quitaron
# CONFIANZA_BASE = 0.6
# NMS_THRESHOLD: 0.30 MIN_CONFIDENCE: 0.60Error %: 15.52538370720189
# MIN_CONFIDENCE: 0.60 Error %: 15.52538370720189
