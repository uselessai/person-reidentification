from re import T
from tkinter import image_names
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
path_180 = "/home/laura/Escritorio/personas_nueva_reid_modelo/280/"
path_000 = "/home/laura/Escritorio/personas_nueva_reid_modelo/000/"
path_distintas = "/home/laura/Escritorio/personas_nueva_reid_modelo/"


ssim_measures = {}
rmse_measures = {}
sre_measures = {}

umbral_similitud = 0.95

scale_percent = 100 # percent of original img size
width = 200 #int(test_img.shape[1] * scale_percent / 100)
height = 50 #int(test_img.shape[0] * scale_percent / 100)
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
for imagen_name in os.listdir(path_180):

    
    image_path_180 = os.path.join(path_180, imagen_name)
    img_180 = cv2.imread(image_path_180) # imagen original
    resized_img_180 = cv2.resize(img_180, dim, interpolation = cv2.INTER_AREA)
    
    imagen_name_000 = imagen_name.split("_")[0] + "_" + "000" + "_" + imagen_name.split("_")[2] + "_" + imagen_name.split("_")[3] + "_" + imagen_name.split("_")[4]
   
    image_path_000 = os.path.join(path_000, imagen_name_000)
    img_000 = cv2.imread(image_path_000) # imagen original
  
    resized_img_000 = cv2.resize(img_000, dim, interpolation = cv2.INTER_AREA)

    SSIM = ssim(resized_img_180, resized_img_000)
    value = "{:.2f}".format(SSIM)
    print (str(contador) + "_" + value)    
    if (SSIM <= umbral_similitud): # si es menor que el umbral descartar la imagen
        contador = contador + 1
        shutil.move(image_path_000, path_distintas + imagen_name)
        shutil.move(image_path_180, path_distintas + imagen_name.split(".")[0] + "_280" + ".png")



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
#p+rint("The most similar according to SRE: " , sre)
90