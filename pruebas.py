import utils.io_image as io
from skimage.io import imread
from PIL import Image
from utils.template_matching import scaled_images_bank

# img = io.read_image("data/images/reloj.jpg")
# img_descarga = Image.fromarray(img)
# img_descarga.save("data/images/reloj_gris.jpg")

img = io.read_image("data/images/nube.jpg")
img_escaladas = scaled_images_bank(3,img)
print(img_escaladas[0])
print(img)
# print(len(img_escaladas))
# img_descarga1 = Image.fromarray(img_escaladas[0])
# img_descarga2 = Image.fromarray(img_escaladas[1])
# img_descarga3 = Image.fromarray(img_escaladas[2])
# img_descarga1.save("data/images/nube1.jpg")
# img_descarga2.save("data/images/nube2.jpg")
# img_descarga3.save("data/images/nube3.jpg")
# io.planes_print(img_escaladas,["1","2","3"],filas = 1, columnas = len(img_escaladas))