# %%
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
#from simpledbf import Dbf5
#import datetime as date 
from carga import ingest_callable

#directorio_parquet = ('datasets/yellow_tripdata_2018-01.parquet')
#directorio_Location = ('./datasets/taxi+_zone_lookup.csv')
#directorio_calendar=('./datasets/calendar.csv')

def transform(directorio_parquet,directorio_Location,directorio_calendar, execution_date):
    #crear dataframe
    df = pd.read_parquet(directorio_parquet)
    df_Taxi_zone = pd.read_csv(directorio_Location)
    calendar = pd.read_csv(directorio_calendar, sep=';')

#------------------------------------------------------------------------------------------------------
    ## Partir data set para rendimiento

    #df = df.iloc[:100000]

#------------------------------------------------------------------------------------------------------


    ## NORMALIZACION
    # copia del df
    df_changes =df.copy()
    # reemplazo valores nulos 
    df_changes['congestion_surcharge'].fillna(0.0, inplace=True)
    df_changes['airport_fee'].fillna(0.0, inplace=True)

    # resto las columnas que no usaremos o dropeamos
    df_changes['total_amount_1'] = df_changes.total_amount - df_changes.tolls_amount - df_changes.congestion_surcharge - df_changes.airport_fee
    df_changes.drop(['congestion_surcharge','airport_fee'], axis=1, inplace=True)
    df_changes['Travel_time'] = df_changes.tpep_dropoff_datetime - df_changes.tpep_pickup_datetime
    # creo columna de location
    df_changes['LocationID']=df_changes['PULocationID']

    # DF Taxi_zone
    # Reemplazo valores nulos
    df_Taxi_zone['Zone'].fillna('Not specified',inplace=True)
    df_Taxi_zone['service_zone'].fillna('Not specified',inplace=True)
    # realizo merge para tener todo en un solo df
    df_changes= df_changes.merge(df_Taxi_zone, how='left', on='LocationID')

    # reseteo el index para renemobarlo y cambiarle el nombre a IdTaxis
    df_changes.reset_index(inplace=True)
    df_changes.rename(columns={'index':'IdTaxis_2018'}, inplace=True)
    #normalizo todos los nombres de los ID 
    df_changes.rename(columns={ 'VendorID':'IdVendor','RatecodeID':'IdRatecode','PULocationID':'IdPULocation','DOLocationID':'IdDOLocation',
                                'payment_type':'IdPayment_type','LocationID':'IdLocation'},inplace=True)

    # en la columna de tpep_pickup_datetime hay fechas mayores al mes de Enero, realizo un drop
    df_changes.drop(df_changes[df_changes['tpep_pickup_datetime'] > '2018-02-01'].index, inplace = True)

    # Creo tabla de Hechos "taxi_trip_2018"
    taxi_trip_2018 = df_changes[:][[   'IdTaxis_2018','IdVendor','tpep_pickup_datetime','tpep_dropoff_datetime','Travel_time','IdRatecode','IdPULocation'
                                    ,'IdDOLocation','IdPayment_type','Borough','fare_amount','extra','mta_tax','tip_amount','improvement_surcharge','total_amount_1']]

    ## CREACION TABLAS DE DIMENCION
    vendor={    1:'Creative Mobile Technologies, LLC',
                2:'VeriFone Inc'}

    vendor = pd.DataFrame([[key, vendor[key]] for key in vendor.keys()], columns=['IdVendor', 'Name_vendor'])


    Ratecode={  1:'Tarifa estándar',
                2:'jfk',
                3:'nuevaark',
                4:'nassau o westchester',
                5:'tarifa negociada',
                6:'paseo en grupo'}

    Ratecode = pd.DataFrame([[key, Ratecode[key]] for key in Ratecode.keys()], columns=['IdRatecode', 'Name_ratecode'])

    payment={   1:'tarjeta de crédito',
                2:'efectivo',
                3:'sin cargo',
                4:'disputa',
                5:'desconocido',
                6:'viaje anulado'}

    payment = pd.DataFrame([[key, payment[key]] for key in payment.keys()], columns=['IdPayment_type', 'Payment_type'])


    Borough_dic = [ {'IdBorough':1,'Borough':'EWR','Latitude':40.6895314,'Longitude':-74.17446239999998},
                    {'IdBorough':2,'Borough':'Queens','Latitude':40.742054,'Longitude':-73.769417},
                    {'IdBorough':3,'Borough':'Bronx','Latitude':40.837048,'Longitude':-73.865433},
                    {'IdBorough':4,'Borough':'Manhattan','Latitude':40.776676,'Longitude':-73.971321},
                    {'IdBorough':4,'Borough':'Staten Island','Latitude':40.579021,'Longitude':-74.151535},
                    {'IdBorough':6,'Borough':'Brooklyn','Latitude':40.650002,'Longitude':-73.949997}]

    Borough = pd.DataFrame(Borough_dic)
    # Funcion para relacionar los indices de una columna con otra
    def algo(params):
        try:
            return Borough.IdBorough[Borough.Borough== params].iloc[0]
        except:
            return 7

    # subescribo los valores del df "df_Taxi_zone" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
    df_Taxi_zone.Borough = df_Taxi_zone.Borough.apply(algo)
    # renombro la columna 
    df_Taxi_zone.rename(columns={'Borough':'IdBorough'}, inplace=True)
    # realizo un drop de la columna "service_zone"
    df_Taxi_zone.drop('service_zone',axis=1 ,inplace=True)
    ## tabla de dimencion "Location"
    Location = df_Taxi_zone.copy()

    ##normalizo la columna "Date" del "calendario" con la forma "AAAA-MM-DD"
    #calendar["Date"] = pd.to_datetime(calendar["date"])
    ## renombro columna id de "calendario"
    #calendar.rename(columns={'id':'IdCalendar'}, inplace=True)
    ## organizo las columnas 
    #calendar = calendar.reindex(columns=['IdCalendar','Date','year','week','day','hour'])

    # Funcion para relacionar los indices de una columna con otra para la tabla taxi_trip_2018
    #def algo1(params):
    #    try:
    #        return Borough.IdBorough[Borough.Borough== params].iloc[0]
    #    except:
    #        return 7
    # subescribo los valores del df "taxi_trip_2018" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
    taxi_trip_2018.Borough = taxi_trip_2018.Borough.apply(algo)     #1)----------------------------------------------
    # Cambio el nombre de la columna "Borough" 
    taxi_trip_2018.rename(columns={'Borough':'IdBorough'}, inplace=True)

    
    #lista_table=[Borough, Location,Ratecode,payment,vendor, calendar, taxi_trip_2018] 
    lista_table = []
    lista_table.append(taxi_trip_2018)
    #print(type(lista_table))
    #print(type(lista_table[0]))
    #print(lista_table[0].head())
#
    #return lista_table

#### ------------------------------------------------------------------------

    # INSERTAR DATAFRAME
    host = 'mypostgres'
    user = 'postgres'
    password = 'postgres'
    port = '5432'
    db = 'ny_taxi'

    ingest_callable(user, password, host, port, db, ['yellow_taxi_trip'], lista_table, execution_date)