# importar librerias
import numpy as np
import pandas as pd
import ast

# cargar datos
df = pd.read_csv('Dataset.csv', sep=',', encoding='utf-8', decimal='.')

# eliminar duplicados
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True) # reset index

# cambiar tipo de datos
df.id = df.id.astype('object')
df.releaseDate = pd.to_datetime(df['releaseDate'], format='%Y-%m-%d')

# imputar valores nulos
df['genre'].fillna(value='No Data', inplace=True)
df['language'].fillna(value='No Data', inplace=True)
df['productionCompany'].fillna(value='No Data', inplace=True)
df['productionCountry'].fillna(value='No Data', inplace=True)
df['cast'].fillna(value='No Data', inplace=True)
df['director'].fillna(value='No Data', inplace=True)

###########

from fastapi import FastAPI

#http://127.0.0.1:8000
#.\venv\Scripts\activate
#uvicorn main:app --reload

app = FastAPI()

@app.get('/')        
def welcome():
    return {'mensaje': 'hola'}

#######

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):

    lista=['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    nmes=lista.index(mes)+1
    respuesta=(df['releaseDate'].dt.month==nmes).sum().astype(str)
    
    return {'mes':mes, 'cantidad':respuesta}

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):

    list_dia=['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    ndia=list_dia.index(dia)
    respuesta=(df['releaseDate'].dt.dayofweek==ndia).sum().astype(str)
    
    return {'dia':dia, 'cantidad':respuesta}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):

    funcion_3 = df[df['title']==titulo][['releaseYear', 'score']]
    funcion_3.reset_index(drop=True, inplace=True)
    respuesta_1 = funcion_3['releaseYear'][0].astype(str)
    respuesta_2 = funcion_3['score'][0].astype(str)
    
    return {'titulo':titulo, 'anio':respuesta_1, 'popularidad':respuesta_2}

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    
    funcion_4 = df[df['title']==titulo][['releaseYear', 'votes', 'rating']]
    funcion_4.reset_index(drop=True, inplace=True)
    respuesta_1 = funcion_4['releaseYear'][0].astype(str)
    respuesta_2 = funcion_4['votes'][0].astype(str)
    respuesta_3 = funcion_4['rating'][0].astype(str)

    if funcion_4['votes'][0] >= 2000:
        return {'titulo':titulo, 'anio':respuesta_1, 'voto_total':respuesta_2, 'voto_promedio':respuesta_3}
    else:
        return {'mensaje':'No cumple con votacion igual o mayor a 2000 votos'}  
    
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):

    funcion_5 = df[df['cast'].str.contains(nombre_actor)][['id', 'return']]
    funcion_5.reset_index(drop=True, inplace=True)    
    respuesta_1 = funcion_5['id'].count().astype(str)
    respuesta_2 = round(funcion_5['return'].sum(), 2)
    respuesta_3 = round(funcion_5['return'].mean(), 2)
    
    return {'actor':nombre_actor, 'cantidad_filmaciones':respuesta_1, 'retorno_total':respuesta_2, 'retorno_promedio':respuesta_3}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):

    funcion_6 = df[df['director'].str.contains(nombre_director)][['id', 'title', 'releaseYear', 'budget', 'revenue', 'return']]
    funcion_6.reset_index(drop=True, inplace=True) 
    respuesta_1 = funcion_6['return'].sum()
    respuesta_2 = funcion_6['title'].tolist()
    respuesta_3 = funcion_6['releaseYear'].tolist()
    respuesta_4 = funcion_6['return'].tolist()
    respuesta_5 = funcion_6['budget'].tolist()
    respuesta_6 = funcion_6['revenue'].tolist()

    indice = funcion_6['id'].tolist()
    pelis=[]
    data={}

    for i in indice:
        j=indice.index(i)
        pelis.append({'titulo': respuesta_2[j], 'anio':respuesta_3[j], 'retorno_pelicula':respuesta_4[j], 'budget_pelicula':respuesta_5[j], 'revenue_pelicula':respuesta_6[j]})

    return {'director':nombre_director, 'retorno_total_director':respuesta_1, 'peliculas': pelis}