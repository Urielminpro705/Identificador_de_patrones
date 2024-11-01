import numpy as np
from skimage.color import rgb2gray

def template_matching(img : np.array, smaller_img : np.array, border_color = [255,0,0], border = 5, optimized = False, new_size = 100):
    img_grey = rgb2gray(img)
    smaller_img_grey = rgb2gray(smaller_img)
    h, w = img.shape[:2]
    sh, sw = smaller_img.shape[:2]

    if h < sh or w < sw:
        print("La imagen a buscar es mas pequeña que la imagen objetivo")
        return {}
    else:
        if optimized:
            sh = new_size
            sw = new_size
            cut_result = cut_img(smaller_img_grey, sw)
            smaller_img_grey = cut_result[0]

        h_iteracion = h - sh + 1
        w_iteracion = w - sw + 1
        ssd = np.zeros((h_iteracion,w_iteracion))
        # Valor, fila, columna
        more_similar = [float("inf"),0,0]
        for f in range(h_iteracion):
            for c in range(w_iteracion):
                section = img_grey[f:f+sh, c:c+sw]
                valor = np.sum((section - smaller_img_grey)**2)
                ssd[f,c] = valor
                if valor < 0.4:
                    more_similar = [valor,f,c]
                    break
                if valor < more_similar[0]:
                    more_similar = [valor,f,c]

        sh, sw, _ = smaller_img.shape
        _, f, c = more_similar
        if optimized:
            f -= cut_result[2]
            c -= cut_result[1] 
        # Top
        img[f:f+border, c:c+sw] = border_color
        # Bottom
        img[f+sh-border:f+sh, c:c+sw] = border_color
        # Start
        img[f:f+sh, c:c+border] = border_color
        # End
        img[f:f+sh, c+sw-border:c+sw] = border_color

        response = {
            "ssd": ssd,
            "image": img
        }
        return response

def cut_img(img : np.array, size = 100):
    h,w = img.shape
    if h > size and w > size:
        margin_start = (w-size)//2
        margin_top = (h-size)//2
        img = img[margin_top:size+margin_top, margin_start:size+margin_start]
    else:
        margin_start = 0
        margin_top = 0
    return [img,margin_start,margin_top]

# img = np.array([
#     [[1,2,3],[4,5,6],[7,8,9]],
#     [[10,11,12],[13,14,15],[16,17,18]],
#     [[19,20,21],[22,23,24],[25,26,27]]
# ])

# smaller_img = np.array([
#     [[10,11,12],[13,14,15]],
#     [[19,20,21],[22,23,24]]
# ])

# response = template_matching(img, smaller_img)
# print(response.get("image"))