import sqlite3
import os  
import pandas as pd


def mapear_datos(nombre_bd, sqlite): #buscar los datos donde se encuentra la base de datos
    carpeta = os.path.dirname(__file__)
    db_path = os.path.join(carpeta, '..', 'data', f'{nombre_bd}{sqlite}')
    return db_path
    
def cargar_datos(ruta_archivo): # Cargar los datos
    conn = sqlite3.connect(ruta_archivo)
    
    dataframes = {}
    
    tablas = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', conn) #Selección de la tabla de la base de datos
    
    for tabla in tablas['name']:
        dataframes[tabla] = pd.read_sql(f'SELECT * FROM "{tabla}"', conn)
    
    conn.close()   #cierre
    
    return dataframes