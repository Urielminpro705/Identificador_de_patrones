from utils import io_image as io
from PIL import Image

img = io.read_image("data/images/reloj.jpg")
img_descarga = Image.fromarray(img)
img_descarga.save("data/images/reloj_gris.jpg")