import glob  # Import glob module to find pathnames
from PIL import Image  # Import Image module from PIL package to work with images
from os.path import basename  # Import basename function from os.path module to get the base name of the file
import os  # Import os module to work with the operating system
import sys  # Import sys module to access some variables used or maintained by the interpreter and to interact with the interpreter
from pathlib import Path  # Import Path module from pathlib package to work with directories and files paths

# Define the original and the destination folder paths
originalesStylegan3 = (r'/home/laura/Escritorio/stylegan3/_noviembre2022')
destinoStylegan3 = (r'/home/laura/Escritorio/stylegan3/_noviembre22_resize/')

# Create a list of all the files and folders inside the original folder
contenido = os.listdir(originalesStylegan3)

# Create a list to store the names of all the images
imagenes = []

# Define the new height and width for the images
new_width = 64
new_height = 128

# Loop through all the folders in the original folder
for folders in contenido:
    # Get the full path of the current folder
    folder_path = os.path.join(originalesStylegan3, folders)

    # Loop through all the files in the current folder
    for fichero in os.listdir(folder_path):
        # Check if the current file is a png file
        if os.path.isfile(os.path.join(folder_path, fichero)) and fichero.endswith('.png'):
            # Open the current image file and resize it to the new dimensions
            img = Image.open(os.path.join(folder_path, fichero))
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Get the current dimensions of the image
            w, h = img.size

            # Get the number at the start of the file name
            fich = int(fichero.split("_")[0])

            # Create a subfolder name using the number at the start of the file name
            subfoldername = "2" + f"{fich:04d}"

            # Create the subfolder if it does not already exist
            if (not os.path.exists(destinoStylegan3 + subfoldername)):
                os.makedirs(destinoStylegan3 + subfoldername)

            # Save the image as a jpg file in the destination folder
            img.crop((0, 0, w, h)).save(os.path.join(destinoStylegan3 + subfoldername, Path(fichero).stem + ".jpg"))

# Print the list of all the image names
print(imagenes)
