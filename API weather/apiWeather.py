# %%
from urllib import request
from urllib import error
import os
import csv
import codecs
import pandas as pd
import numpy as np

# %%
initial_date = '2018-01-01'
final_date = '2018-01-01'
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20York/" + initial_date + "/" + final_date + "?unitGroup=metric&include=hours&key=HB4HE49PF5XCRSEHAULTVM73D&contentType=csv"

# %%
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


# %%
a = []

# %%
for i in CSVText:
  a.append(i)


# %%
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

# %%
df.drop(['name','stations'], axis=1,inplace=True)


# Cambiaremos el contenido de la columna "icon" especificando unicamente si es de dia o de noche

def day_night(icon):
    return icon.split('-')[-1]

# %%
df.icon = df.icon.apply(day_night)


# La tabla de hechos sera df como weather y separaremos las columnas "condition" y "icon" para crear 2 dimensiones; condition y icon, respectivamente.

# %%
condition = pd.DataFrame()

# %%
condition['condicion'] = df.conditions.unique()



# %%
icon = pd.DataFrame()

# %%
icon['estado'] = df.icon.unique()


# Reemplazar los valores de tabla main por los valores de id en las tablas dimensionales



# %%
def estado (i):
    s = i.split('-')[-1]
    return (icon[icon.estado == s].index[0])

def cond (i):
    s = i.split('-')[-1]
    return (condition[condition.condicion == s].index[0])

# %%
df.icon = df.icon.apply(estado)

# %%
df.conditions = df.conditions.apply(cond)



# %% [markdown]
# Cambiamos todos los tipos de dato a strings



# %%
for i in df:
    df[i] = df[i].astype('string')



# %%
icon.estado = icon.estado.astype('string')
condition.condicion = condition.condicion.astype('string')

# %% [markdown]
# Crear todos los csv de weather, icon y condition.

# %%
df.to_csv('weather.csv')
icon.to_csv('icono.csv')
condition.to_csv('condicion.csv')


