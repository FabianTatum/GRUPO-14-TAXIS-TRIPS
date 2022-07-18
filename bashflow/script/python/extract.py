#!/bin/bash/env python

from urllib import request
from urllib import error
import sys
import csv
import codecs
import pandas as pd
from datetime import datetime as dt



print(f'[{str(dt.now())[:19]}] - Search data from source...')
initial_date = '2018-01-01'
final_date = '2018-01-01'
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20York/" + initial_date + "/" + final_date + "?unitGroup=metric&include=hours&key=FWHEEXHLDYZDXTKVGHP2SSCWL&contentType=csv"
try:
    #ResultBytes = urllib.request.urlopen("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20York/2018-01-01/2018-01-01?unitGroup=metric&include=hours&key=HB4HE49PF5XCRSEHAULTVM73D&contentType=csv")
    ResultBytes = request.urlopen(url)
    # Parse the results as CSV
    CSVText = csv.reader(codecs.iterdecode(ResultBytes, 'utf-8'))
    # Parse the results as JSON
    #jsonData = json.loads(ResultBytes.decode('utf-8'))
except error.HTTPError  as e:
    ErrorInfo= e.read().decode() 
    print('Error code: ', e.code, ErrorInfo)
    sys.exit()
except  error.URLError as e:
    ErrorInfo= e.read().decode() 
    print('Error code: ', e.code,ErrorInfo)
    sys.exit()


a = []

for i in CSVText:
    a.append(i)


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

df.drop(['name','stations'], axis=1,inplace=True)


# Cambiaremos el contenido de la columna "icon" especificando unicamente si es de dia o de noche

def day_night(icon):
    return icon.split('-')[-1]

df.icon = df.icon.apply(day_night)

# La tabla de hechos sera df como weather y separaremos las columnas "condition" y "icon" para crear 2 dimensiones; condition y icon, respectivamente.
condition = pd.DataFrame()

condition['condition'] = df.conditions.unique()

icon = pd.DataFrame()
icon['state'] = df.icon.unique()

# Reemplazar los valores de tabla main por los valores de id en las tablas dimensionales
def estado (i):
    s = i.split('-')[-1]
    return (icon[icon.state == s].index[0])

def cond (i):
    s = i.split('-')[-1]
    return (condition[condition.condition == s].index[0])

df.icon = df.icon.apply(estado)

df.conditions = df.conditions.apply(cond)

# Cambiamos todos los tipos de dato a strings
#for i in df:
#    df[i] = df[i].astype('string')

icon.state = icon.state.astype('string')
condition.condition = condition.condition.astype('string')

# pasar datos a datetime
df['datetime'] = pd.to_datetime(df['datetime'])
# Borrar columnas innecesarias
df.drop(columns=['dew', 'windgust', 'precipprob', 'preciptype', 'winddir', 'sealevelpressure', 'cloudcover', 
                'visibility', 'solarradiation', 'solarenergy', 'uvindex', 'severerisk', 'snowdepth'], inplace=True)


# index
icon['IdIcon'] = icon.index
condition['IdCondition'] = condition.index

# renombrar claves
df.rename(columns={'conditions': 'IdCondition', 'icon': 'IdIcon'}, inplace=True)

#Crear los esquemas de tablas
table = './script/sql/schema.sql'

# Crear todos los csv de weather, icon y condition.
with open(table, 'a') as f:
    f.write('\n' + pd.io.sql.get_schema(df, name='weather') + '\n' + ';')
df.to_csv('./out/weather.csv', index=False)
print(f'[{str(dt.now())[:19]}] - Extract data from weather successfuly.')
with open(table, 'a') as f:
    f.write('\n' + pd.io.sql.get_schema(icon, name='icon') + '\n' + ';')
icon.to_csv('./out/icon.csv',  index=False)
print(f'[{str(dt.now())[:19]}] - Extract data from icon successfuly.')
with open(table, 'a') as f:
    f.write('\n' + pd.io.sql.get_schema(condition, name='condition') + '\n' + ';')
condition.to_csv('./out/condition.csv', index=False)
print(f'[{str(dt.now())[:19]}] - Extract data from condition successfuly.')

print(f'[{str(dt.now())[:19]}] - EXTRACT DATA FROM SOURCE SUCCESSFULY')