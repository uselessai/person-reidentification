import cv2
import os
import imutils
from sys import argv
import matplotlib.pyplot as plt
import shutil  
import numpy as np


import json

with open('/home/laura/Escritorio/stylegan3/_screenshots/editor_imgs/Stylegan3_MarketTodas_3440_FID50k.jsonl', 'r') as json_file:
    json_list = list(json_file)
    

#for json_str in json_list:
    #result = json.loads(json_str)
    #print(f"result: {result}")
    #print(isinstance(result, dict))

with open('/home/laura/Escritorio/stylegan3/_screenshots/editor_imgs/Stylegan3_MarketTodas_3440_FID50k.jsonl', 'r') as json_file:  
    data = [json.loads(line) for line in json_file]


result = [] 
metrica = []

for i in range(len(data)):
    result.append(data[i]['results']['fid50k_full'])
    value = data[i]['snapshot_pkl']
    value_met = value.split("-")[2].split(".")[0] # para obtener el número de imágenes
    metrica.append(int(value_met))


plt.plot( metrica,result, color="red")
plt.show()