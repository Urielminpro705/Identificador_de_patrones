import numpy as np

def template_matching(img : np.array, smaller_img : np.array, color_marco = [255,0,0], grosor_marco = 5):
    h, w, can = img.shape
    sh, sw, can = smaller_img.shape

    if h < sh or w < sw:
        print("La imagen a buscar es mas pequeña que la imagen objetivo")
        return {}
    else:
        h_iteracion = h - sh + 1
        w_iteracion = w - sw + 1
        ssd = np.zeros((h_iteracion,w_iteracion))
        # Valor, fila, columna
        mas_parecido = [float("inf"),0,0]
        for f in range(h_iteracion):
            for c in range(w_iteracion):
                seccion = img[f:f+sh, c:c+sw]
                menor = np.sum((seccion - smaller_img)**2)
                ssd[f,c] = menor
                if menor < mas_parecido[0]:
                    mas_parecido = [menor,f,c]
                    if menor == 0:
                        break
        
        _, f, c = mas_parecido
        img_out = img[f:f+sh, c:c+sw, :]

        # Top
        img[f:f+grosor_marco, c:c+sw] = color_marco
        # Bottom
        img[f+sh-grosor_marco:f+sh, c:c+sw] = color_marco
        # Start
        img[f:f+sh, c:c+grosor_marco] = color_marco
        # End
        img[f:f+sh, c+sw-grosor_marco:c+sw] = color_marco

        response = {
            "ssd": ssd,
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