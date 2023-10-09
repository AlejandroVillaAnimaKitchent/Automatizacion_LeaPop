import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from itertools import compress


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     


st.write("# ¡Bienvenido a la Automatización de Canales Para Lea & Pop! :ocean::pirate_flag: :ocean:")

# st.sidebar.success("Selecciona una tarea:")

st.markdown(
    """
    Este es el Hub que contendrá todas las herramientas necesarias para facilitar la creación y la gestión de nuevos supercanales.
    Esta apliación esta todavía en desarrollo, úsala bajo tu propia responsabilidad. :warning:
        
    Si te encuentras con un problema contacta con: pablo.perezmartin@animakitchent.com o alejandro.villa@animakitchent.com. :email:
        
    Sé explícito con lo que te ocurre e incluye un vídeo o captura de pantalla del problema a ser posible. 
    En el menú de arriba a la derecha (tres barras horizontales), tienes herramientas para sacar capturas de pantalla y vídeos. :camera: 
        
        
    **👈 Elige una tarea a la izquierda 👈** 
    """
)
    

    
    
# if 'thumbs_by_song' not in st.session_state:
#     st.session_state['thumbs_by_song'] = []
# else:
# st.text(str(len(st.session_state['thumbs_by_song'])))
# st.text(str(len(st.session_state['selected_videos'])))
# if 'song_thumb_list' not in st.session_state:
#     st.session_state['song_thumb_list'] = []
# else:
#      st.text(str(len(st.session_state['song_thumb_list'])))
# if 'song_thumb_list' not in st.session_state:
#     st.session_state['song_thumb_list'] = []
# else:
#      st.text(str(len(st.session_state['song_thumb_list'])))
# if 'song_thumb_list' not in st.session_state:
#     st.session_state['song_thumb_list'] = []
# else:
#      st.text(str(len(st.session_state['song_thumb_list'])))
# if 'song_thumb_list' not in st.session_state:
#     st.session_state['song_thumb_list'] = []
# else:
#      st.text(str(len(st.session_state['song_thumb_list'])))

# if 'a' not in st.session_state:
#     a = 'patata'

# if st.button('Pulsa'):
#     st.sidebar.text(a)
    
    
# import psutil
 
# Getting % usage of virtual_memory ( 3rd field)
# st.info('RAM memory % used:'+ str(psutil.virtual_memory()[2]))
# Getting usage of virtual_memory in GB ( 4th field)
# st.info('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)

# # URL of the image
# url = 'http://img.youtube.com/vi/zc_GmIvLkjE/mqdefault.jpg' 

# # Send HTTP request to URL and save the response from server in a response object called r
# response = requests.get(url)

# # Create an Image object from an Image file, or an Image object
# img = Image.open(BytesIO(response.content))

# # Display the image using Streamlit
# st.image(img, caption='Your caption here')

