import numpy as np

def template_matching(img : np.array, smaller_img : np.array):
    h, w, _ = img.shape
    sh, sw, _ = smaller_img.shape

    if h < sh or w < sw:
        print("La imagen a buscar es mas pequeña que la imagen objetivo")
        return {}
    else:
        h_iteracion = h - sh + 1
        w_iteracion = w - sw + 1
        ssd = np.zeros((h_iteracion,w_iteracion))

        for f in range(h_iteracion):
            for c in range(w_iteracion):
                seccion = img[f:f+sh, c:c+sw]
                ssd[f,c] = np.sum((seccion - smaller_img)**2)

        response = {
            "doesExist" : False,
            "Image": None
        }
        print(ssd)
        return response


img = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])

smaller_img = np.array([
    [4,5],
    [7,8]
])

template_matching(img, smaller_img)