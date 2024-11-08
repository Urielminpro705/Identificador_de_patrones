from skimage.color import rgb2gray
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt

def read_image(image_path):
    #Leer la imagen
    img = imread(image_path)
    #Si esta a color la convertimos a escala de gris
    if len(img.shape) == 3:
        img = rgb2gray(img)
        img = (img * 255).astype(np.uint8) #Convertimos a int de 8 bits sin signo
    else:
        img = img.astype(np.uint8)

    return img

def quantize(img : np.array, L : int):
    q_img = np.floor((img/255)*(2**L-1)).astype(np.uint8)
    return q_img

#Lista para almacenar los diferentes niveles de cuantizacion
def quantize_all(img):
    quantized_imgs = []
    for i in range(8,0,-1):
        q_img = quantize(img, i)
        quantized_imgs.append(q_img)
    return quantized_imgs

def extract_bit_planes(img):
    height, width = img.shape
    bit_planes = np.zeros((8,height,width), np.uint8)
    for a in range(height):
        for b in range(width):
            pixel_value = img[a,b]
            lineaBits = f"{pixel_value:08b}"
            for c in range(0,8):
                bit_planes[c,a,b] = int(lineaBits[c])*255 
    return bit_planes # lista de imagenes

def image_bit_combination(img, planesList):
    bit_planes = np.flip(extract_bit_planes(img), axis=0)
    height, width = bit_planes[0].shape
    changedPlanes = np.zeros((len(planesList),height,width),np.uint8)
    for i in range(len(planesList)):
        dec = 2**planesList[i]
        for a in range(height):
            for b in range(width):
                changedPlanes[i,a,b] = dec if bit_planes[planesList[i],a,b] == 255 else 0
    return np.sum(changedPlanes, axis=(0))

def planes_print(bit_planes,titulos, filas, columnas):
    figura, eje = plt.subplots(filas,columnas)
    cont = 0
    if filas == 1:
        for c in range(columnas):
            eje[c].axis('off')
            if cont != len(bit_planes):
                eje[c].imshow(bit_planes[cont], cmap='grey')
                try:
                    eje[c].set_title(titulos[cont])
                except:
                    pass
                cont += 1
    else:
        for f in range(filas):
            for c in range(columnas):
                eje[f,c].axis('off')
                if cont != len(bit_planes):
                    eje[f,c].imshow(bit_planes[cont], cmap='grey')
                    try:
                        eje[f,c].set_title(titulos[cont])
                    except:
                        pass
                    cont += 1
    plt.tight_layout()
    plt.show()

def print_img(img, titulo):
    plt.imshow(img, cmap='grey')
    plt.suptitle(titulo)
    plt.axis('off')
    plt.show()