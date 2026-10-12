import csv
import unicodedata
from pathlib import Path

import streamlit as st

st.set_page_config(page_title='Certificados de participación | III CCEm 2026', page_icon='📜', layout='centered')


def normalizar(valor):
    texto = unicodedata.normalize('NFKD', str(valor).casefold())
    return ''.join(c for c in texto if not unicodedata.combining(c))


@st.cache_data
def cargar():
    ruta = Path(__file__).parent / 'participacion_drive.csv'
    with ruta.open(encoding='utf-8-sig', newline='') as archivo:
        filas = list(csv.DictReader(archivo))
    return [f for f in filas if f.get('Nombre del participante') and f.get('ID de Drive')]


st.title('Certificados de participación')
st.markdown('**III Congreso Colombiano de Etnomatemática**')
st.caption('Riohacha, 6 al 8 de octubre de 2026')
st.write('Escribe tu nombre o apellido para encontrar tu certificado de participación.')

try:
    filas = cargar()
except Exception:
    st.error('No se encontró el archivo de datos participacion_drive.csv en la aplicación.')
    st.stop()

busqueda = st.text_input('Nombre o apellido', placeholder='Escribe al menos 3 letras')
if busqueda.strip():
    if len(busqueda.strip()) < 3:
        st.info('Escribe al menos tres letras para buscar.')
    else:
        encontrados = [f for f in filas if normalizar(busqueda.strip()) in normalizar(f['Nombre del participante'])]
        st.caption(f'{len(encontrados)} certificado(s) encontrado(s)')
        for f in sorted(encontrados, key=lambda x: normalizar(x['Nombre del participante'])):
            nombre = f['Nombre del participante']
            id_drive = f['ID de Drive'].strip()
            enlace = 'https://drive.google.com/file/d/' + id_drive + '/view'
            st.markdown('---')
            st.markdown(f'**{nombre}** — Participación')
            st.link_button('Abrir o descargar certificado (Google Drive)', enlace)
        if not encontrados:
            st.info('No encontramos un certificado con ese nombre. Comprueba la escritura o consulta con la organización.')

st.divider()
st.caption('Los certificados de ponencia se consultan en el buscador de ponentes. Los documentos se alojan en Google Drive.')
