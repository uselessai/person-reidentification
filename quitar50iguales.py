import cv2
import os
import image_similarity_measures
import imutils
import shutil  
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
import matplotlib.pyplot as plt

import numpy as np

path_stylegan = "/home/laura/Escritorio/stylegan3/_screenshots/artificiales/"
path_descartadas = "/home/laura/Escritorio/stylegan3/_screenshots/descartadas/"
data_dir = path_stylegan

solo_uno = True
eliminar = 20

for folder2 in sorted(os.listdir(data_dir)):
	if (solo_uno):
		
            #solo_uno = False
		folder_path = os.path.join(data_dir, folder2)
		index = 0		
		#for file in sorted(os.listdir(folder_path)): # lista ordenada por nombre
		for file in os.listdir(folder_path):
			
			if (index >= eliminar):
				img_path = os.path.join(folder_path + "/", file)
				new_path = path_descartadas + folder2 + "_Deja20"
				if not (os.path.isdir(new_path)): os.mkdir(new_path)
				shutil.move(img_path, new_path)
			index = index + 1
           