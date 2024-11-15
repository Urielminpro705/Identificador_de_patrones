import numpy as np
from skimage.color import rgb2gray
from skimage.transform import resize
from abc import ABC, abstractmethod

class Template_Matching(ABC):
    def __init__(self):
        self.img = None
        self.smaller_img = None
        self.img_grey = None
        self.smaller_img_grey = None
        self.h = None
        self.w = None
        self.sw = None
        self.sh = None
        self.progress_bar = None
        self.optimized = False
        self.new_size = 100
        self.more_similar = None
        self.cut_result = None
        self.border_color = [255,0,0]
        self.border = 5
        pass
    
    def __grayscale(self):
        if len(self.img.shape) > 2:
            self.img_grey = rgb2gray(self.img)
        else:
            self.img_grey = self.img
            self.img = np.stack((self.img,) * 3, axis = -1)
        if len(self.smaller_img.shape) > 2:
            self.smaller_img_grey = rgb2gray(self.smaller_img)
        else:
            self.smaller_img_grey = self.smaller_img
            self.smaller_img = np.stack((self.smaller_img,) * 3, axis = -1)

    def size_check(self):
        self.h, self.w = self.img_grey.shape
        self.sh, self.sw = self.smaller_img_grey.shape
        if self.h < self.sh or self.w < self.sw:
            print("La imagen a buscar es mas pequeña que la imagen objetivo")
            self.progress_bar.empty()
            return False
        return True

    def is_optimized(self):
        if self.optimized:
            cut_result = cut_img(self.smaller_img_grey, self.new_size)
            self.sh = self.new_size if cut_result[2] != 0 else self.sh
            self.sw = self.new_size if cut_result[1] != 0 else self.sw
            self.smaller_img_grey = cut_result[0]

    @abstractmethod
    def sdc(self):
        h_iteration = self.h - self.sh + 1
        w_iteration = self.w - self.sw + 1
        ssd = np.zeros((h_iteration,w_iteration))
        total_iterations = h_iteration*w_iteration
        update_interval = total_iterations // 10
        if update_interval == 0:
            update_interval = 1
        completed_iterations = 0

        # Valor, fila, columna
        self.more_similar = [float("inf"),0,0]
        for f in range(h_iteration):
            for c in range(w_iteration):
                section = self.img_grey[f:f+self.sh, c:c+self.sw]
                value = np.sum((section - self.smaller_img_grey)**2)
                ssd[f,c] = value
                completed_iterations += 1
                if self.progress_bar:
                    if completed_iterations % update_interval == 0:
                        progress_percentage = int((completed_iterations / total_iterations) * 100)
                        self.progress_bar.progress(progress_percentage, "Buscando...")
                if value < 0.4:
                    more_similar = [value,f,c]
                    break
                if value < more_similar[0]:
                    more_similar = [value,f,c]
        
        self.sh, self.sw, _ = self.smaller_img.shape
    
    def add_frame(self):
        _, f, c = self.more_similar
        if self.optimized:
            f -= self.cut_result[2]
            c -= self.cut_result[1]

        # Top
        self.img[f:f+self.border, c:c+self.sw] = self.border_color
        # Bottom
        self.img[f+self.sh-self.border:f+self.sh, c:c+self.sw] = self.border_color
        # Start
        self.img[f:f+self.sh, c:c+self.border] = self.border_color
        # End
        self.img[f:f+self.sh, c+self.sw-self.border:c+self.sw] = self.border_color
        if self.progress_bar:
            self.progress_bar.progress(100, "Completado")


def template_matching(img : np.array, smaller_img : np.array, border_color = [255,0,0], border = 5, optimized = False, new_size = 100, progress_bar=None):
    # Conversion a escala de grises
    if len(img.shape) > 2:
        img_grey = rgb2gray(img)
    else:
        img_grey = img
        img = np.stack((img,) * 3, axis = -1)
        print(f"Imagen original {img_grey.shape}")
    if len(smaller_img.shape) > 2:
        smaller_img_grey = rgb2gray(smaller_img)
        print(f"Seccion: {smaller_img_grey.shape}")
        print(smaller_img)
        print(smaller_img_grey)
    else:
        smaller_img_grey = smaller_img
        smaller_img = np.stack((smaller_img,) * 3, axis = -1)
    
    # Comprobar tamaño
    h, w = img_grey.shape
    sh, sw = smaller_img_grey.shape
    if h < sh or w < sw:
        print("La imagen a buscar es mas pequeña que la imagen objetivo")
        progress_bar.empty()
        return {}
    else:
        if optimized:
            cut_result = cut_img(smaller_img_grey, new_size)
            sh = new_size if cut_result[2] != 0 else sh
            sw = new_size if cut_result[1] != 0 else sw
            smaller_img_grey = cut_result[0]

        h_iteration = h - sh + 1
        w_iteration = w - sw + 1
        ssd = np.zeros((h_iteration,w_iteration))
        total_iterations = h_iteration*w_iteration
        update_interval = total_iterations // 10
        if update_interval == 0:
            update_interval = 1
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

def scaled_images_bank(levels : int, img : np.array):
    h,w = img.shape
    gap = 100/levels
    percent = 100
    sizes = [percent]
    resized_images = []
    for i in range(levels-1):
        percent -= gap
        sizes.append(percent)
    
    for i in sizes:
        w *= (i/100)
        h *= (i/100)
        resized_image = resize(img, (h,w), preserve_range=True)
        resized_images.append(resized_image)
    return resized_images

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