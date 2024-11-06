import streamlit as st
from skimage import io
from utils.template_matching import template_matching
import numpy as np

def iniciar_busqueda():
    st.session_state.button_disabled = True
    with progress_bar_cont:
        progress_text = "Buscando..."
        progress_bar = st.progress(0, text=progress_text)
    if img_objetivo_uploader is not None and seccion_img_uploader is not None:
        response = template_matching(img_objetivo, seccion_img, optimized=optimized, new_size=30, progress_bar=progress_bar)
        img_out = response.get("image")
        if img_out is not None:
            with result_cont:
                st.subheader("Resultado")
                st.image(img_out, caption="Resultado")
        else:
            with result_cont:
                st.warning("La imagen a buscar debe ser mas pequeña que la imagen objetivo")
    st.session_state.button_disabled = False

st.title("Identificador de patrones")
img_objetivo_uploader = st.file_uploader("Elige una imagen objetivo", type=['jpg', 'jpeg'])
seccion_img_uploader = st.file_uploader("Elige la imagen a buscar", type=['jpg', 'jpeg'])

col1,col2 = st.columns([0.5,0.5], gap="small", vertical_alignment="top")

optimized = st.toggle("Optimizar (Recomendado para imagenes muy grandes)", value = False)
progress_bar_cont = st.container()

if img_objetivo_uploader is not None:
    img_objetivo = io.imread(img_objetivo_uploader)
    with col1:
        st.subheader("Donde buscar")
        st.image(img_objetivo, caption="Imagen Objetivo")

if seccion_img_uploader is not None:
    seccion_img = io.imread(seccion_img_uploader)
    with col2:
        st.subheader("Que buscar")
        st.image(seccion_img, caption="Seccion a buscar")

if seccion_img_uploader is not None and img_objetivo_uploader is not None:
    st.session_state.button_disabled = False
else:
    st.session_state.button_disabled = True

st.button(key="buscar", on_click=iniciar_busqueda, label="Buscar", type="primary", use_container_width=True, disabled=st.session_state.button_disabled)
result_cont = st.container()