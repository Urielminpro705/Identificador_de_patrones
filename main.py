import streamlit as st
from skimage import io, color
from skimage import img_as_float
from utils.template_matching import template_matching
import numpy as np

st.title("Buscador de patrones")
img_objetivo_uploader = st.file_uploader("Elige una imagen objeivo", type=['jpg', 'jpeg','png'])
seccion_img_uploader = st.file_uploader("Elige la imagen a buscar", type=['jpg', 'jpeg','png'])

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

if img_objetivo_uploader is not None and seccion_img_uploader is not None:
    response = template_matching(img_objetivo, seccion_img)
    img_out = response.get("image")
    st.header("Resultado")
    st.image(img_out, caption="Resultado")