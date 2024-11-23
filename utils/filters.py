import numpy as np

def conv2d(img, k):
    hk,wk = k.shape
    if not hk % 2:
        print("El tamaño del kernel tiene que ser un numero impar")
        return img
    else:
        h,w = img.shape
        k_rotado = np.rot90(k, k=2)
        padding = hk // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                img_out[f,c] = np.sum(k_rotado * padding_img[f:(f+hk),c:(c+wk)])
        return img_out

def filtro_promedio(n):
    if n % 2:
        k = np.ones((n,n))/(n**2)
        return k
    else:
        print("Kernel size should be an odd number")

def gaussian_kernel(sigma=1, n=3):
    if n % 2 == 0:
        raise ValueError("Kernel size should be an odd number")
    
    # Define grid of (x, y) coordinates
    a = -(n // 2)
    b = n // 2
    x, y = np.meshgrid(np.arange(a, b + 1), np.arange(a, b + 1))

    # Compute Gaussian function
    g = 1 / (2 * np.pi * sigma**2) * np.exp(-((x**2 + y**2) / (2 * sigma**2)))

    # Normalize so that the sum of the kernel is 1
    g /= g.sum()

    return g

def media_aritmetica(img, w_size):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                img_out[f,c] = np.mean(padding_img[f:(f+w_size),c:(c+w_size)])
    return img_out

def media_geometrica(img, w_size):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        img = img.astype(np.float64)
        h,w = img.shape
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                img_out[f,c] = np.prod(padding_img[f:(f+w_size),c:(c+w_size)])**(1/(w_size**2))
    return img_out

def media_armonico(img, w_size):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                img_out[f,c] =  (w_size**2)/np.sum(1/padding_img[f:f+w_size, c:c+w_size])
    return img_out

def media_contraarmonico(img, w_size, q):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        img = img.astype(np.float64)
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                img_out[f,c] =  np.sum(padding_img[f:f+w_size, c:c+w_size]**(q+1))/np.sum(padding_img[f:f+w_size, c:c+w_size]**q)
    return img_out

def mediana(img, w_size):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        img = img.astype(np.float64)
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                ventana = padding_img[f:f+w_size, c:c+w_size]
                img_out[f,c] = np.median(ventana)
    return img_out

def max(img, w_size):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        img = img.astype(np.float64)
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                ventana = padding_img[f:f+w_size, c:c+w_size]
                img_out[f,c] = np.max(ventana)
    return img_out

def min(img, w_size):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        img = img.astype(np.float64)
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                ventana = padding_img[f:f+w_size, c:c+w_size]
                img_out[f,c] = np.min(ventana)
    return img_out

def media_recortada(img, w_size, alpha):
    if not w_size % 2:
        print("El tamaño del filtro debe ser impar")
        return img
    else:
        h,w = img.shape
        img = img.astype(np.float64)
        padding = w_size // 2
        img_out = np.zeros((h,w))
        padding_img = np.pad(img, pad_width=padding)
        for f in range(h):
            for c in range(w):
                ventana = padding_img[f:f+w_size, c:c+w_size]
                ventana_ordenada = np.sort(ventana, axis=None)
                img_out[f,c] = np.sum(ventana_ordenada[alpha:-alpha])/((w_size**2)-(alpha*2))
    return img_out
# img = np.array([
#     [15,13,13],
#     [23,27,23],
#     [23,27,23],
# ])

# img_out = media_aritmetica(img, 3)
# print(img_out)