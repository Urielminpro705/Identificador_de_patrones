import streamlit as st
from skimage import io
from utils.template_matching import template_matching
import numpy as np

st.title("Identificador de patrones")
img_objetivo_uploader = st.file_uploader("Elige una imagen objetivo", type=['jpg', 'jpeg'])
seccion_img_uploader = st.file_uploader("Elige la imagen a buscar", type=['jpg', 'jpeg'])

col1,col2 = st.columns([0.5,0.5], gap="small", vertical_alignment="top")

if img_objetivo_uploader is not None:
    img_objetivo = io.imread(img_objetivo_uploader)
    with col1:
        st.header("Donde buscar")
        st.image(img_objetivo, caption="Imagen Objetivo")

if seccion_img_uploader is not None:
    seccion_img = io.imread(seccion_img_uploader)
    with col2:
        st.header("Que buscar")
        st.image(seccion_img, caption="Seccion a buscar")

if seccion_img_uploader is not None and img_objetivo_uploader is not None:
    st.session_state.button_disabled = False
else:
    st.session_state.button_disabled = True

def iniciar_busqueda():
    st.session_state.button_disabled = True
    if img_objetivo_uploader is not None and seccion_img_uploader is not None:
        response = template_matching(img_objetivo, seccion_img, optimized=True, new_size=50)
        img_out = response.get("image")
        with result_cont:
            st.header("Resultado")
            st.image(img_out, caption="Resultado")
    st.session_state.button_disabled = False

st.button(key="buscar", on_click=iniciar_busqueda, label="Buscar", type="primary", use_container_width=True, disabled=st.session_state.button_disabled)
result_cont = st.container()