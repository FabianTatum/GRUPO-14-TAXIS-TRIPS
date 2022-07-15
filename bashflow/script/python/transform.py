#!/bin/bash/env python

import pandas as pd
import numpy as np
#from simpledbf import Dbf5
import datetime as date 

print('-----------------------------------')
print('|||     CARGANDO EN PARQUET     |||')
print('-----------------------------------')

df = pd.read_parquet('./in/yellow_trips_2018-01.parquet')

# del df

print('PARQUET CSV CON EXITO')

print(df.head(5))

df_copy = df.sample(500000)

# creo una nueva columna del monto total restando las posibles columnas que no vamos a usar 
df_copy['total_amount_1'] = df_copy.total_amount - df_copy.tolls_amount - df_copy.congestion_surcharge - df_copy.airport_fee

df_copy.drop(['congestion_surcharge','airport_fee'], axis=1, inplace=True)


# creo nueva columna del tiempo de vieja desde que sube al taxis hasta que baja
df_copy['Travel_time'] = df_copy.tpep_dropoff_datetime - df_copy.tpep_pickup_datetime

df_copy.isna().sum()

df_copy['LocationID']=df_copy['PULocationID']

# columnas de dias y horas

df_copy['day'] = df_copy['tpep_pickup_datetime'].map(lambda x: x.weekday()+1)
df_copy['hour'] = df_copy['tpep_pickup_datetime'].map(lambda x: x.hour)
conditionlist = [
    (df_copy['hour']<6),
    (df_copy['hour']<13),
    (df_copy['hour']<19),
    (df_copy['hour']<24)]
turnos = ['late_night', 'morning', 'afternoon', 'night']
df_copy['turno'] = np.select(conditionlist, turnos, default='Not Specified')


# levanto la tabla de los borough
df_Taxi_zone = pd.read_csv('./in/taxi_zone_lookup.csv')

df_Taxi_zone['Zone'].fillna('Not specified',inplace=True)
df_Taxi_zone['service_zone'].fillna('Not specified',inplace=True)


# realizo el merge
df_copy = df_copy.merge(df_Taxi_zone, how='left', on='LocationID')


# no se si sirva pero ahi esta una tabla con las columnas que creo importante, quiza falten algunas mas para realizar los calculos
df_costos = df_copy[['LocationID','Borough','Zone','trip_distance','total_amount_1','payment_type','Travel_time','hour','day','turno']]
df_costos


df_copy['IdTaxis'] = df_copy.index

df_copy.rename(columns={ 'VendorID':'IdVendor','RatecodeID':'IdRatecode','PULocationID':'IdPULocation','DOLocationID':'IdDOLocation',
                            'payment_type':'IdPayment_type','LocationID':'IdLocation'},inplace=True)


taxi_trip_2018 = df_copy[['IdTaxis','IdVendor','tpep_pickup_datetime','tpep_dropoff_datetime','Travel_time','IdRatecode','IdPULocation'
                           ,'IdDOLocation','IdPayment_type', 'fare_amount','extra','mta_tax','tip_amount','improvement_surcharge','total_amount_1']]

to_str = lambda x: str(x)

taxi_trip_2018['Travel_time'] = taxi_trip_2018['Travel_time'].apply(to_str)

dx = taxi_trip_2018[taxi_trip_2018['IdRatecode'] > 10].index
taxi_trip_2018.drop(index=dx, inplace=True)

print('---------------------------------')
print('|||    CONVIRTIENDO TRIPS     |||')
print('---------------------------------')

table = './script/sql/schema.sql'
# TODO: Tabla de Viajes
print('Convert to csv Taxi Trips')
with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(taxi_trip_2018, name='taxi_trips') + ';' + '\n')
taxi_trip_2018.to_csv('./out/taxi_trips.csv', index=False)

print('----------------------------------')
print('|||     CONVIRTIENDO VENDOR    |||')
print('----------------------------------')
# TODO: Tabla Vendor
vendor={    1:'Creative Mobile Technologies, LLC',
            2:'VeriFone Inc'}

df_vendor = pd.DataFrame([[key, vendor[key]] for key in vendor.keys()], columns=['IdVendor', 'Name_vendor'])
with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(df_vendor, name='vendor') + ';' + '\n')
df_vendor.to_csv('./out/vendor.csv', index=False)

# 1= Tarifa estándar, **2**= jfk, **3**= nuevaark, **4**= nassau o westchester, **5**= tarifa negociada, **6**= paseo en grupo

print('---------------------------------')
print('|||   CONVIRTIENDO RATECODE   |||')
print('---------------------------------')
# TODO: Tabla Rate Code
Ratecode={  1:'Tarifa estándar',
            2:'jfk',
            3:'nuevaark',
            4:'nassau o westchester',
            5:'tarifa negociada',
            6:'paseo en grupo'}

df_Ratecode = pd.DataFrame([[key, Ratecode[key]] for key in Ratecode.keys()], columns=['IdRatecode', 'Name_ratecode'])


with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(df_Ratecode, name='ratecode') + '\n' + ';')
df_Ratecode.to_csv('./out/ratecode.csv', index=False)

# **1= tarjeta de crédito, **2**= efectivo, **3**= sin cargo, **4**= disputa, **5**= desconocido, **6**= viaje anulado**

print('---------------------------------')
print('|||   CONVIRTIENDO PAYMENTS   |||')
print('---------------------------------')
# TODO: Tabla Payment
payment={   1:'tarjeta de crédito',
            2:'efectivo',
            3:'sin cargo',
            4:'disputa',
            5:'desconocido',
            6:'viaje anulado'}

df_payment = pd.DataFrame([[key, payment[key]] for key in payment.keys()], columns=['IdPayment_type', 'Payment_type'])
with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(df_payment, name='payment') + '\n' + ';')
df_payment.to_csv('./out/payment.csv', index=False)

print('---------------------------------')
print('|||   CONVIRTIENDO BOROUGH    |||')
print('---------------------------------')
# TODO: Tabla Location
df_copy.rename(columns={'index':'taxis_id'}, inplace=True)

Borough_dic = [ {'IdBorough':1,'Borough':'EWR','Latitude':40.6895314,'Longitude':-74.17446239999998},
                {'IdBorough':2,'Borough':'Queens','Latitude':40.742054,'Longitude':-73.769417},
                {'IdBorough':3,'Borough':'Bronx','Latitude':40.837048,'Longitude':-73.865433},
                {'IdBorough':4,'Borough':'Manhattan','Latitude':40.776676,'Longitude':-73.971321},
                {'IdBorough':5,'Borough':'Staten Island','Latitude':40.579021,'Longitude':-74.151535},
                {'IdBorough':6,'Borough':'Brooklyn','Latitude':40.650002,'Longitude':-73.949997},
                {'IdBorough':7,'Borough':'Unknown','Latitude':0.0,'Longitude':0.0}]

Borough = pd.DataFrame(Borough_dic)
with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(Borough, name='borough') + ';' + '\n' )
Borough.to_csv('./out/borough.csv', index=False)


def algo(params):
    return Borough.IdBorough[Borough.Borough== params].iloc[0]

df_Taxi_zone.Borough = df_Taxi_zone.Borough.apply(algo)
df_Taxi_zone.rename(columns={'Borough':'IdBorough', 'LocationID': 'IdLocation'}, inplace=True)
df_Taxi_zone.drop('service_zone',axis=1 ,inplace=True)

print('---------------------------------')
print('|||   CONVIRTIENDO LOCATION   |||')
print('---------------------------------')
Location = df_Taxi_zone.copy()
with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(Location, name='location') + ';' + '\n' )
Location.to_csv('./out/location.csv', index=False)

print('---------------------------------')
print('|||   CONVIRTIENDO CALENDAR   |||')
print('---------------------------------')
# TODO: Tabla Calendario
def calendar_table(start='', end=''):
    df = pd.DataFrame({'Date':pd.date_range(start, end)})
    df['Year'] = df.Date.dt.year
    df['Month'] = df.Date.dt.month
    df['Day'] = df.Date.dt.day
    df['Week'] = df.Date.dt.isocalendar().week
    df['Weekday'] = df.Date.dt.day_of_week + 1
    return df

calendar = calendar_table('2018-01-01', '2018-01-31')
with open(table, "a") as f:
    f.write('\n' + pd.io.sql.get_schema(calendar, name='calendar') + '\n' + ';')
calendar.to_csv('./out/calendar.csv', index=False)

'''
calendar.rename(columns={'id':'IdCalendar'}, inplace=True)

type(calendar.IdCalendar[calendar.date == str('1/1/2018').split(' ')[0]].loc[0])

taxi_trip_2018['IdCalendar']= 0

taxi_trip_2018.IdCalendar = taxi_trip_2018.tpep_dropoff_datetime.apply(id_tabla)

# subescribo los valores del df "taxi_trip_2018" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
taxi_trip_2018.Borough = taxi_trip_2018.Borough.apply(algo)
# Cambio el nombre de la columna "Borough" 
taxi_trip_2018.rename(columns={'Borough':'IdBorough'}, inplace=True)
'''