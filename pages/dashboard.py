import sys 
from pathlib import Path 
import streamlit as st 
import plotly.express as px 
import pandas as pd

#llamamo la bbdd que vamos a utilizar
root = Path(__file__).parent.parent
sys.path.append(str(root))

from utils.dependencias import *

path_chinook = mapear_datos('Chinook', '.sqlite')

dataframes = cargar_datos(path_chinook) #se carga en un dataframe

#llamamos las tablas que necesitamos para el análisis
tracks_table = dataframes['Track']
albums_table = dataframes['Album']
artists_table = dataframes['Artist']
invoice_items_table = dataframes['InvoiceLine']
invoices_table = dataframes['Invoice']
customers_table = dataframes['Customer']
genres_table = dataframes['Genre']

st.header("Dashboard")


# 1. Preparar los datos necesarios
# Unir tablas para obtener información necesaria
datos = (
    invoice_items_table
    .merge(tracks_table, on='TrackId')
    .merge(albums_table, on='AlbumId')
    .merge(artists_table, on='ArtistId')
    .merge(invoices_table, on='InvoiceId')
    .merge(genres_table, on='GenreId')
    .merge(customers_table, on='CustomerId')
)

# Renombrar columnas para mayor claridad
datos = datos.rename(columns={
    'Name': 'Artista',
    'Title': 'Album',
    'InvoiceDate': 'Fecha',
    'Quantity': 'Cantidad',
    'Total': 'Total',
    'Name_y': 'Genero',
    'Country': 'Pais'
})

# Convertir la columna Fecha a formato datetime
datos['Fecha'] = pd.to_datetime(datos['Fecha'])

# Agregar una columna para un nuevo cálculo basado en cantidad y una métrica adicional
datos['NuevoCalculo'] = datos['Cantidad'] * 2  # Ejemplo de cálculo: duplicar la cantidad

# filtros dinámicos
st.sidebar.header("Filtros")

## Filtro por rango de fechas
fecha_min = datos['Fecha'].min()
fecha_max = datos['Fecha'].max()
rango_fechas = st.sidebar.date_input(
    "Rango de Fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)

## Filtro por artista
artistas_unicos = datos['Artista'].unique()
artista_seleccionado = st.sidebar.multiselect(
    "Artistas",
    options=artistas_unicos,
    default=artistas_unicos,
)

## Filtro por género musical
generos_unicos = datos['Genero'].unique()
genero_seleccionado = st.sidebar.multiselect(
    "Géneros Musicales",
    options=generos_unicos,
    default=generos_unicos,
)

## Filtro por país
paises_unicos = datos['Pais'].unique()
pais_seleccionado = st.sidebar.multiselect(
    "Países",
    options=paises_unicos,
    default=paises_unicos,
)

# 3. Aplicar las máscaras para filtrar los datos
mask = (
    (datos['Fecha'] >= pd.to_datetime(rango_fechas[0])) &
    (datos['Fecha'] <= pd.to_datetime(rango_fechas[1])) &
    (datos['Artista'].isin(artista_seleccionado)) &
    (datos['Genero'].isin(genero_seleccionado)) &
    (datos['Pais'].isin(pais_seleccionado))
)

datos_filtrados = datos[mask]

# 4. Cálculo de métricas
total_artistas = datos_filtrados['Artista'].nunique()
total_albumnes = datos_filtrados['Album'].nunique()
total_paises = datos_filtrados['Pais'].nunique()

# Mostrar métricas en Streamlit
st.subheader("Métricas Generales")

col1, col2, col3 = st.columns(3)
with st.container():
      
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total de Artistas",
            value=total_artistas
        )

    with col2:
        st.metric(
            label="Total de Álbumes",
            value=total_albumnes
        )

    with col3:
        st.metric(
            label="Total de Países",
            value=total_paises
        )
        
st.divider()

# 5. Generar gráficos

## Gráfico 1: Barras horizontales - Métrica seleccionada por artista

metrica_por_artista = (
    datos_filtrados.groupby('Artista', as_index=False)
    .agg({'Total': 'sum'})
    .sort_values(by='Total', ascending=False)
)

fig_barras = px.bar(
    metrica_por_artista,
    x='Total',
    y='Artista',
    orientation='h',
    title='Total por Artista',
    labels={'Total': 'Total', 'Artista': 'Artista'},
    color='Total',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_barras)

container = st.container(border=True)
container.write("El gráfico anterior nos muestra que género músical es más popular y"
                "cual es el que las personas menos consumen.")
    
st.divider()

## Gráfico 3: Dispersión - Métrica seleccionada vs. cantidad de pistas
metrica_vs_pistas = (
    datos_filtrados.groupby('Album', as_index=False)
    .agg({'Cantidad': 'sum', 'Total': 'sum'})
)

fig_dispersion = px.scatter(
    metrica_vs_pistas,
    x='Cantidad',
    y='Total',
    size='Total',
    color='Album',
    title='Total vs. Cantidad de Pistas',
    labels={'Cantidad': 'Cantidad de Pistas', 'Total': 'Total', 'Album': 'Álbum'}
)
st.plotly_chart(fig_dispersion)

container = st.container(border=True)
container.write("El gráfico anterior nos muestra que pista músical es más popular y"
                "cual es el que las personas menos se reproduce.")

st.divider()

## Gráfico 1: Barras verticales - Métrica seleccionada por país y artista
metrica_por_pais_artista = (
    datos_filtrados.groupby(['Pais', 'Artista'], as_index=False)
    .agg({'Total': 'sum'})
    .sort_values(by='Total', ascending=False)
)

fig_barras = px.bar(
    metrica_por_pais_artista,
    x='Pais',
    y='Total',
    color='Artista',
    title='Total por País y Artista',
    labels={'Total': 'Total', 'Artista': 'Artista', 'Pais': 'País'},
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_barras)

container = st.container(border=True)
container.write("El gráfico anterior nos muestra el aporte que nos han hecho los diferentes"
                "países, con sus diferentes artistas y cuál es el país con más artistas.")

st.divider()

st.caption("Creador por :blue[Ing. Katherine GL]")







