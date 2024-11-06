import streamlit as st
from skimage import io
from skimage.color import rgb2gray
from utils.template_matching import template_matching
import numpy as np

def iniciar_busqueda():
    st.session_state.button_disabled = True
    with progress_bar_cont:
        progress_text = "Buscando..."
        progress_bar = st.progress(0, text=progress_text)
    if img_objetivo_uploader is not None and section_img_uploader is not None:
        response = template_matching(img_objetivo, section_img, optimized=optimized, new_size=section_size, progress_bar=progress_bar)
        img_out = response.get("image")
        if img_out is not None:
            with result_cont:
                st.subheader("Resultado")
                st.image(img_out, caption="Resultado")
        else:
            with result_cont:
                st.warning("La imagen a buscar debe ser mas pequeña que la imagen objetivo")
    st.session_state.button_disabled = False

# Titulo de la app
st.title("Identificador de patrones")

# Input de imagenes
img_objetivo_uploader = st.file_uploader("Elige una imagen objetivo", type=['jpg', 'jpeg'])
section_img_uploader = st.file_uploader("Elige la imagen a buscar", type=['jpg', 'jpeg'])

# Columnas para mostrar las dos imagenes subidas
col1,col2 = st.columns([0.5,0.5], gap="small", vertical_alignment="top")

# Switch para activar o desactivar la optimizacion
optimized = st.toggle("Optimizar (Recomendado para imagenes muy grandes)", value = False)

# Slider para el tamaño de recorte
if optimized and section_img_uploader is not None:
    img = io.imread(section_img_uploader)
    size = img.shape[:2]
    smaller = min(size)
    if smaller < 40:
        st.warning("La imagen a buscar ya es muy pequeña")
    else:
        section_size = st.slider("Tamaño de recorte", 30, 200 if smaller >= 200 else smaller)
else:
    section_size = 0

# Contenedor de la barra de progreso
progress_bar_cont = st.container()

# Comprobar si ya existe la imagen objetivo para mostrarla
if img_objetivo_uploader is not None:
    img_objetivo = io.imread(img_objetivo_uploader)
    with col1:
        st.subheader("Donde buscar")
        st.image(img_objetivo, caption="Imagen Objetivo")

# Comprobar si ya existe la seccion a buscar para mostrarla
if section_img_uploader is not None:
    section_img = io.imread(section_img_uploader)
    with col2:
        st.subheader("Que buscar")
        st.image(section_img, caption="Seccion a buscar")

# Comprobar si ya existen las dos imagenes para activar el boton o de lo contrario desactivarlo
if section_img_uploader is not None and img_objetivo_uploader is not None:
    st.session_state.button_disabled = False
else:
    st.session_state.button_disabled = True

# Boton para iniciar la busqueda
st.button(key="buscar", on_click=iniciar_busqueda, label="Buscar", type="primary", use_container_width=True, disabled=st.session_state.button_disabled)

# Contenedor para mostrar la imagen resultante
result_cont = st.container()