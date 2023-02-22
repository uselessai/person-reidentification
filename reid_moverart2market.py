import glob
import os, sys
import shutil 
from pathlib import Path

# CONVERTIMOS LAS IMAGESN A FORMATO JPG Y MODIFICAMOS EL TAMAÑO
path_artificiales = (r'/home/laura/Escritorio/stylegan3/_screenshots/NuevasStyleganCharm10052022/content/images/')
path_market = (r'/home/laura/Escritorio/stylegan3/_screenshots/NuevasStyleganCharm10052022/content/prueba/')
contenido = os.listdir(path_artificiales)
imagenes = []



for folders in contenido:
    folder_path = os.path.join(path_artificiales, folders)
    contador = 0
    for fichero in os.listdir(folder_path):
        if (contador >=5):
            break
        if os.path.isfile(os.path.join(folder_path, fichero)) and fichero.endswith('.jpg'):
            img_path = os.path.join(folder_path + "/", fichero)
            new_path = path_market + folders  + "/"
            shutil.move(img_path, new_path)
        contador = contador + 1

print(imagenes)