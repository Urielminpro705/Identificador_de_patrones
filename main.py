import streamlit as st
from skimage import io, color
import numpy as np

st.title("Buscador de patrones")
img_objetivo_uploader = st.file_uploader("Elige una imagen objeivo", type=['jpg', 'jpeg', 'png'])
seccion_img_uploader = st.file_uploader("Elige la imagen a buscar", type=['jpg', 'jpeg', 'png'])

col1,col2 = st.columns([0.5,0.5], gap="small", vertical_alignment="top")

if img_objetivo_uploader is not None:
    img_objetivo = io.imread(img_objetivo_uploader)
    with col1:
        st.header("Donde buscar")
        st.image(img_objetivo, caption='Imagen Objetivo')

if seccion_img_uploader is not None:
    seccion_img = io.imread(seccion_img_uploader)
    with col2:
        st.header("Que buscar")
        st.image(seccion_img, caption='Seccion a buscar')