import glob
from PIL import Image
from os.path import basename
import os, sys
from pathlib import Path

# CONVERTIMOS LAS IMAGESN A FORMATO JPG Y MODIFICAMOS EL TAMAÑO
originalesStylegan3 = (r'/home/laura/Escritorio/stylegan3/_noviembre2022')
destinoStylegan3 = (r'/home/laura/Escritorio/stylegan3/_noviembre22_resize/')

contenido = os.listdir(originalesStylegan3)
imagenes = []

new_width  = 64 #64
new_height = 128 #64

for folders in contenido:
    folder_path = os.path.join(originalesStylegan3, folders)

    for fichero in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, fichero)) and fichero.endswith('.png'):
            #imagenes.append(fichero)
            img = Image.open(os.path.join(folder_path, fichero))
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            w, h = img.size
            fich = int(fichero.split("_")[0])
            subfoldername = "2" + f"{fich:04d}"
            if (not os.path.exists(destinoStylegan3 + subfoldername)):
                os.makedirs(destinoStylegan3 + subfoldername)
            img.crop((0, 0, w, h)).save(os.path.join(destinoStylegan3 + subfoldername, Path(fichero).stem + ".jpg"))
       
print(imagenes)