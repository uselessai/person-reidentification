import glob
from PIL import Image
from os.path import basename
import os, sys
from pathlib import Path
from sys import argv
import shutil  
import numpy as np



# CONVERTIMOS LAS IMAGENES A FORMATO JPG Y MODIFICAMOS EL TAMAÑO

origen = (r'/home/laura/Escritorio/stylegan3/_screenshots/432IMGsJunio22_resize_descartadas')
destino = (r'/home/laura/Escritorio/stylegan3/_screenshots/432IMGsJunio22_resize/')


origen2 = (r'/home/laura/Escritorio/stylegan3/_noviembre22_resize')
destino2 = (r'/home/laura/Escritorio/stylegan3/_noviembre22_resize_bien/')

def mover_concsv(origen2, destino2):
    # Using readline()
    file1 = open('lista_ordenada_nombre_imagenes.txt', 'r')
    count = 0
    new_width  = 64 #64
    new_height = 128 #64
    while True:
        count += 1
        #"0023_c4s1_004151_01.jpg-Tue Nov  1 19:07:51 2022"
        #"Archivo guardado -/home/laura/Escritorio/stylegan3/_noviembre2022/0000/0000_c3s3_0000_1000.png"
        # Get next line from file

        line1 = file1.readline().strip()
        line2 = file1.readline().strip()
        nombre_archivo = line1.split("-")[0] + "_" +  line2.split("_")[4].split(".")[0]
        nombre_archivo = nombre_archivo.replace(".jpg", "")
        origen = line2.split("-")[1]
        
        img = Image.open(origen)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        w, h = img.size
        

        destino = destino2 + line1.split("_")[0]
        if not (os.path.isdir(destino)): os.mkdir(destino)
        img.crop((0, 0, w, h)).save(os.path.join(destino, Path(nombre_archivo).stem + ".jpg"))


    

        # if line is empty
        # end of file is reached
        if not line2:
            break
        print("Line{}: {}".format(count, line2.strip()))
    
    file1.close()



def mover_todas(origen, destino) :

    for folders in os.listdir(origen):
        folder_path = os.path.join(origen, folders)

        id_folder = folders.split("_")[0]

        for fichero in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, fichero)) and fichero.endswith('.jpg'):
                img_path = os.path.join(folder_path + "/", fichero)
                new_path = destino + id_folder 
                if not (os.path.isdir(new_path)): os.mkdir(new_path)
                shutil.move(img_path, new_path)

def mover_50(origen, destino) :

    for folders in os.listdir(origen):
        folder_path = os.path.join(origen, folders)
        contador = 0
        id_folder = folders.split("_")[0]
        folder_sort = os.listdir(folder_path)
        folder_sort.sort()
        for fichero in folder_sort:
            
            if os.path.isfile(os.path.join(folder_path, fichero)) and fichero.endswith('.jpg') and contador > 50:
                img_path = os.path.join(folder_path + "/", fichero)
                print (img_path)
                new_path = destino + "/" + id_folder + "_50/" # crear carpeta
                if not (os.path.isdir(new_path)): os.mkdir(new_path)
                new_path = new_path + fichero # mover archivo
                shutil.move(img_path, new_path)
            contador = contador + 1
              
        
#mover_todas(origen,destino)
mover_concsv(origen2, destino2)
#mover_50(destino,origen) # quitar las que son iguales