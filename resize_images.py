import os 
from PIL import Image

folder = r"\\cancer\Material_Definitivo\telerin\THUMBNAILS"
folderlow = r"\\cancer\Material_Definitivo\telerin\THUMBNAILS\lowres"
images = [file for file in os.listdir(folder) if file.endswith('png')]
imageslow = [file for file in os.listdir(folderlow) if file.endswith('png')]

for file in images:
    if file not in imageslow:
        img = Image.open(os.path.join(folder,file))
        new_size = (img.width // 2, img.height // 2)   # New size is half the original size
        resized_img = img.resize(new_size)
        resized_img.save(os.path.join(folderlow,file))