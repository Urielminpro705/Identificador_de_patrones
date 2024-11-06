import numpy as np
from skimage.color import rgb2gray
import streamlit as st

def template_matching(img : np.array, smaller_img : np.array, border_color = [255,0,0], border = 5, optimized = False, new_size = 100, progress_bar=None):
    img_grey = rgb2gray(img)
    smaller_img_grey = rgb2gray(smaller_img)
    h, w = img.shape[:2]
    sh, sw = smaller_img.shape[:2]

    if h < sh or w < sw:
        print("La imagen a buscar es mas pequeña que la imagen objetivo")
        progress_bar.empty()
        return {}
    else:
        if optimized:
            sh = new_size
            sw = new_size
            cut_result = cut_img(smaller_img_grey, sw)
            smaller_img_grey = cut_result[0]

        h_iteration = h - sh + 1
        w_iteration = w - sw + 1
        ssd = np.zeros((h_iteration,w_iteration))
        total_iterations = h_iteration*w_iteration
        update_interval = total_iterations // 10
        completed_iterations = 0

        # Valor, fila, columna
        more_similar = [float("inf"),0,0]
        for f in range(h_iteration):
            for c in range(w_iteration):
                section = img_grey[f:f+sh, c:c+sw]
                value = np.sum((section - smaller_img_grey)**2)
                ssd[f,c] = value
                completed_iterations += 1
                if progress_bar:
                    if completed_iterations % update_interval == 0:
                        progress_percentage = int((completed_iterations / total_iterations) * 100)
                        progress_bar.progress(progress_percentage, "Buscando...")
                if value < 0.4:
                    more_similar = [value,f,c]
                    break
                if value < more_similar[0]:
                    more_similar = [value,f,c]
        
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
        if progress_bar:
            progress_bar.progress(100, "Completado")
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