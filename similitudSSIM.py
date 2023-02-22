from re import T
import cv2
import os
import image_similarity_measures
import imutils
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
import matplotlib.pyplot as plt
import shutil  
import numpy as np

img_market = "0002_c1s1_000551_01.jpg" #argv[1]
img_stylegan = "1_1001_00000.jpg"
path_market = "/home/laura/Escritorio/stylegan3/_screenshots/Market1501_train/train_all/"
path_stylegan = "/home/laura/Escritorio/stylegan3/_noviembre22_resize_bien/"
path_descartadas = "/home/laura/Escritorio/stylegan3/_noviembre22_resize_descartadas/"
data_dir = path_market

is_market = False # atenta que mueve las imagenes
if (is_market):
	data_dir = path_market
else:
	data_dir = path_stylegan

test_img = cv2.imread(path_market + "0002/"+ img_market)

ssim_measures = {}
rmse_measures = {}
sre_measures = {}

umbral_similitud = 0.75

scale_percent = 100 # percent of original img size
width = int(test_img.shape[1] * scale_percent / 100)
height = int(test_img.shape[0] * scale_percent / 100)
dim = (width, height)


# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# media y desviación standar..

ssim_aux = []
#histograma = [0] * 10000
solo_uno = True
contador  = 0
contador_todas = 0
for folder2 in os.listdir(data_dir):
	if (solo_uno):

		#solo_uno = False
		folder_path = os.path.join(data_dir, folder2)
		primera_img = True
		
		for file in sorted(os.listdir(folder_path)):
			contador_todas = contador_todas + 1  
			img_path = os.path.join(folder_path + "/", file)
			if (primera_img):
				primera_img = False
				test_img = cv2.imread(img_path) # imagen original
			else:
				data_img = cv2.imread(img_path)
				resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
				SSIM = ssim(test_img, resized_img)
				value = "{:.2f}".format(SSIM)
				ssim_measures[img_path]= value
				ssim_aux.append(value)

				if (SSIM < umbral_similitud): # si es menor que el umbral descartar la imagen
					contador = contador + 1
					if (not is_market):
						new_path = path_descartadas + folder2 + "_SSIM"
						if not (os.path.isdir(new_path)): os.mkdir(new_path)
						shutil.move(img_path, new_path)

				#histograma[round(ssim_measures[img_path], 2) * 100] = histograma[round(ssim_measures[img_path], 2) * 100] + 1
				#rmse_measures[img_path]= rmse(test_img, resized_img)
				#sre_measures[img_path]= sre(test_img, resized_img)
			
			
				                               
	else:
		break




def calc_closest_val(dict, checkMax):
    result = {}
    if (checkMax):
    	closest = max(dict.values())
    else:
    	closest = min(dict.values())
    		
    for key, value in dict.items():
    	print("The difference between ", key ," and the original image is : \n", value)
    	if (value == closest):
    	    result[key] = closest
    	    
    print("The closest value: ", closest)	    
    print("######################################################################")
    return result
    
ssim = calc_closest_val(ssim_measures, True)
#rmse = calc_closest_val(rmse_measures, False)
#sre = calc_closest_val(sre_measures, True)
#aux = sorted(ssim_measures.items(), key=lambda x: x[1])    
ssim_aux.sort()
print ("Se han descartado " + str(contador))
porcentaje = (contador * 100 ) / contador_todas
print ("porcentaje eliminadas " + str(porcentaje))

#plt.hist( *zip(*sorted(ssim_measures.items()))) #, bins = 20)
#bar(myDictionary.keys(), myDictionary.values(), width, color='g')
plt.title('Histograma Market-1501')
plt.xlabel('SSIM')
plt.ylabel('Número de imágenes') 


plt.hist(ssim_aux, bins = 38)
plt.show()


#plt.savefig('/home/laura/Escritorio/stylegan3/_screenshots/editor_imgs/Histogram_SSIM.png')


print("The most similar according to SSIM: " , ssim)
#print("The most similar according to RMSE: " , rmse)
#print("The most similar according to SRE: " , sre)
