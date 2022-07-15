# 
from urllib import request
from urllib import error
import os
import csv
import codecs
import pandas as pd
import numpy as np
from datetime import timedelta
from carga import ingest_callable

def weather(actual_date, execution_date):

    initial_date = str(actual_date)
    final_date = str(pd.to_datetime(actual_date) + timedelta(days = 30)).split(' ')[0]
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20York/" + initial_date + "/" + final_date + "?unitGroup=metric&include=hours&key=B2QLPZ9FVP3VYYG7RTDLN5RGU&contentType=csv"
####B2QLPZ9FVP3VYYG7RTDLN5RGU
####HB4HE49PF5XCRSEHAULTVM73D
    try:
        #ResultBytes = urllib.request.urlopen("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20York/2018-01-01/2018-01-01?unitGroup=metric&include=hours&key=HB4HE49PF5XCRSEHAULTVM73D&contentType=csv")
        ResultBytes = request.urlopen(url)
        # Parse the results as CSV
        CSVText = csv.reader(codecs.iterdecode(ResultBytes, 'utf-8'))
     #Parse the results as JSON
    #jsonData = json.loads(ResultBytes.decode('utf-8')

#--------------------------------------------------------------------------------

#
        a = []
        for i in CSVText:
            a.append(i)


        #
        # Crear dataframe y columnas
        df = pd.DataFrame()
        for idx, i in enumerate(a[0]):
            df[i] = a[1][idx]


        # Agregar los registros al dataframe
        first = False
        for idx, i in enumerate(a):
            if first:
                df.loc[idx] = i
            else:
                first = True


        # Elimminar columnas "Nombre" y "station" pues no sirven para nuestro analisis

        #
        df.drop(['name','stations'], axis=1,inplace=True)


        # Cambiaremos el contenido de la columna "icon" especificando unicamente si es de dia o de noche

        def day_night(icon):
            return icon.split('-')[-1]

        #
        df.icon = df.icon.apply(day_night)


        # La tabla de hechos sera df como weather y separaremos las columnas "condition" y "icon" para crear 2 dimensiones; condition y icon, respectivamente.

        ##
        #condition = pd.DataFrame()
    #
        ##
        #condition['condicion'] = df.conditions.unique()
    #

        icon ={
            0: 'night',
            1: 'day'}
        icon = pd.DataFrame([[key, icon[key]] for key in icon.keys()], columns=['Idcondicion', 'condicion'])
        # -------------------------------------------------------------------------------

        condition = pd.read_csv('logs/conditions_weather.csv')
        condition = condition.reset_index()
        condition.rename(columns={'index':'id_condition','id':'key_api'}, inplace=True)


        # Reemplazar los valores de tabla main por los valores de id en las tablas dimensionales



        #
        def dia (i):
            return (icon[icon.condicion == i].index[0])

        def cond (i):
            return (condition[condition.desc == i].index[0])

        #
        df.icon = df.icon.apply(dia)

        #
        df.conditions = df.conditions.apply(cond)

        lista_table = [df]
        # INSERTAR DATAFRAME
        host = 'mypostgres'
        user = 'postgres'
        password = 'postgres'
        port = '5432'
        db = 'ny_taxi'

        ingest_callable(user, password, host, port, db, ['weather'], lista_table, execution_date)


        # %% [markdown]
        # Cambiamos todos los tipos de dato a strings



        #
        #for i in df:
        #    df[i] = df[i].astype('string')



        #
        #icon.estado = icon.estado.astype('string')
        #condition.condicion = condition.condicion.astype('string')

        # %% [markdown]
        # Crear todos los csv de weather, icon y condition.

        #
        #df.to_csv('weather.csv')
        #icon.to_csv('icono.csv')
        #condition.to_csv('condicion.csv')

    ##---------------------------------------------------------


    except error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        #sys.exit()
    except  error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        #sys.exit()


    


