import numpy as np
from skimage.color import rgb2gray

def template_matching(img : np.array, smaller_img : np.array, border_color = [255,0,0], border = 10, optimized = False):
    img_grey = rgb2gray(img)
    smaller_img_grey = rgb2gray(smaller_img)
    h, w = img.shape[:2]
    sh, sw = smaller_img.shape[:2]

    if h < sh or w < sw:
        print("La imagen a buscar es mas pequeña que la imagen objetivo")
        return {}
    else:
        if optimized and (sh > 100 and sw > 100):
            sh = 50
            sw = 50
            smaller_img_grey = smaller_img_grey[:sh, :sw]

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
        # Top
        img[f:f+border, c:c+sw] = border_color
        # Bottom
        img[f+sh-border:f+sh, c:c+sw] = border_color
        # Start
        img[f:f+sh, c:c+border] = border_color
        # End
        img[f:f+sh, c+sw-border:c+sw] = border_color

        response = {
            "more_similar_list": ssd,
            "image": img
        }
        return response

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