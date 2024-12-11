import streamlit as st 
# import plotly.express as px 
import time
import sqlite3

st.title("_Dashboard_ Chinook ")
st.markdown("*Análisis* de **datos**.")


container = st.container(border=False)
container.write("La base de datos Chinook contiene información detallada sobre clientes, facturación, álbumes, pistas, géneros y artistas." 
                "Para abordar las preguntas planteadas, se utilizarán tablas como Invoice, Track, Album, Artist, Genre y InvoiceLine para" 
                "obtener los datos necesarios sobre las ventas, el contenido de los álbumes y las características de los artistas y géneros musicales.")

container = st.container(border=False)
container.write("¿Cómo varían las ventas totales a lo largo del tiempo?")
container = st.container(border=False)
container.write("Se busca identificar patrones estacionales en las ventas de música,"
                "lo que permitirá planificar mejor los lanzamientos de productos y las campañas de marketing.")

container = st.container(border=False)
container.write("¿Cuál es la relación entre el número de pistas en un álbum y las ventas totales de ese álbum?")
container = st.container(border=False)
container.write("Este análisis tiene como objetivo identificar el número óptimo de pistas que favorezca un mayor volumen de"
                "ventas, lo cual es clave para los productores y artistas al decidir la estructura de los álbumes.")

container = st.container(border=False)
container.write("¿Qué factores o períodos han influido más en las ventas por artista y por álbum?")
container = st.container(border=False)
container.write("A través de la comparación de ventas entre artistas, géneros y años, se pretende encontrar"
                "correlaciones que permitan entender mejor el comportamiento de los consumidores y predecir períodos de alta demanda.")

container = st.container(border=False)
container.write("¿Cómo la digitalización y las plataformas de streaming afectan las ventas de música?")
container = st.container(border=False)
container.write("Analizando el comportamiento de las ventas a lo largo de los años, se identificarán los años"
                " clave en los que las plataformas de streaming y otros factores tecnológicos influyeron en el rendimiento de las ventas")

st.caption("Creador por :blue[Ing. Katherine GL]")