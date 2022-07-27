#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt
from logs import log


PG_HOST = '127.0.0.1'
PG_USER = 'root'
PG_PASSWORD = 'root'
PG_PORT = "5432"
PG_DATABASE = "ny_taxi"

def conn(query):
    '''
    Return:
    --------------
    Retorna un diccionario con las tablas en postgres heroku
    '''
    log('Iniciando conexion a base de datos...')
    engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')
    conn = engine.connect()
    log('Conexion Exitosa.')
    
    table = pd.read_sql(query, con=engine)
    log('Tabla cargada exitosamente.')

    # Cierre de conexion
    conn.close()
    engine.dispose()

    return table