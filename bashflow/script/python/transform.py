import pandas as pd
from datetime import datetime as dt
import sample_data as sd
from pandarallel import pandarallel
from logs import log

#funcion para calcular outliers
def outliers_obt(data, columna,cuartial1,cuartil2,valoriqr=1.5):
    ##calculamos los cuartiles 
    Q1 = data[columna].quantile(float(cuartial1))
    #print('Primer Cuartile', Q1)
    Q3 = data[columna].quantile(float(cuartil2))
    #print('Tercer Cuartile',Q3)
    IQR = Q3 - Q1
    #print('Rango intercuartile', IQR)

    ##calculamos los bigotes superior e inferior
    BI = (Q1 - valoriqr * IQR)
    #print('bigote Inferior \n', BI)
    BS = (Q3 + valoriqr * IQR)
    #print('bigote superior \n', BS)

    ##obtenemos una nueva tabla sin los outliers
    ubi_sin_out = data[(data[columna] >= BI) & (data[columna] <= BS)]
    return ubi_sin_out

def transform(fecha):
    directorio_parquet = (f'./in/yellow_trips_{fecha}.parquet')
    directorio_Location = ('./in/taxi_zone_lookup.csv')
    #directorio_calendar=('./in/calendar.csv')

    #crear dataframe
    log('WARNING: Parquet charge in memory initialized !!!')
    df_org = pd.read_parquet(directorio_parquet)
    log('SUCCESS: Parquet charge in memory completed.\n')
    df_Taxi_zone = pd.read_csv(directorio_Location)
    #calendar = pd.read_csv(directorio_calendar, sep=';')
    
    log('SUCCESS: Parquet charge in memory completed.\n')

    df = sd.muestra(df_org, fecha)
    #df = df_org.sample(1000000)
    del df_org

    log('Transform data initialized.\n')
    log('Please wait...\n')

    ## NORMALIZACION
    df=outliers_obt(df,'total_amount','0.25','0.75',valoriqr=4.5)
    df=outliers_obt(df,'improvement_surcharge','0.25','0.75',valoriqr=4.5)
    df=outliers_obt(df,'tip_amount','0.25','0.75',valoriqr=2)
    df=outliers_obt(df,'mta_tax','0.25','0.75',valoriqr=1.5)
    df=outliers_obt(df,'extra','0.25','0.75',valoriqr=1.5)
    df=outliers_obt(df,'fare_amount','0.25','0.75',valoriqr=4.5)
    df=outliers_obt(df,'trip_distance','0.25','0.75',valoriqr=3)
    df=outliers_obt(df,'tpep_dropoff_datetime','0.25','0.75',valoriqr=1.5)
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

    mask = df_changes['IdRatecode'] < 10
    df_changes = df_changes[mask] 

    # Creo tabla de Hechos "taxi_trip_2018"
    taxi_trip_2018 = df_changes[[  'IdTaxis_2018','IdVendor', 'tpep_pickup_datetime', 'tpep_dropoff_datetime','trip_distance','Travel_time','IdRatecode','IdPULocation'
                                    ,'IdDOLocation','IdPayment_type','Borough','IdLocation','fare_amount','extra','mta_tax','tip_amount','improvement_surcharge','total_amount_1']]

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
                    {'IdBorough':5,'Borough':'Staten Island','Latitude':40.579021,'Longitude':-74.151535},
                    {'IdBorough':6,'Borough':'Brooklyn','Latitude':40.650002,'Longitude':-73.949997},
                    {'IdBorough':7,'Borough':'Unknown','Latitude':0.0,'Longitude':0.0}]

    Borough = pd.DataFrame(Borough_dic)
    # Funcion para relacionar los indices de una columna con otra
    def algo(params):
        try:
            return Borough.IdBorough[Borough.Borough== params].iloc[0]
        except:
            return 7

    #def algo(params):
    #    if params == 'EWR':
    #        return 1
    #    if params == 'Queens':
    #        return 2
    #    if params == 'Bronx':
    #        return 3
    #    if params == 'Manhattan':
    #        return 4
    #    if params == 'Staten Island':
    #        return 5
    #    if params == 'Brooklyn':
    #        return 6
    #    else:
    #        return params

    # subescribo los valores del df "df_Taxi_zone" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
    pandarallel.initialize()
    df_Taxi_zone.Borough = df_Taxi_zone.Borough.parallel_apply(algo)
    #df_Taxi_zone.Borough = df_Taxi_zone.Borough.apply(algo)
    # renombro la columna 
    df_Taxi_zone.rename(columns={'Borough':'IdBorough', 'LocationID': 'IdLocation'}, inplace=True)
    # realizo un drop de la columna "service_zone"
    df_Taxi_zone.drop('service_zone',axis=1 ,inplace=True)
    # subescribo los valores del df "taxi_trip_2018" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
    taxi_trip_2018.Borough = taxi_trip_2018.Borough.parallel_apply(algo)
    # Cambio el nombre de la columna "Borough" 
    taxi_trip_2018.rename(columns={'Borough':'IdBorough'}, inplace=True)
    ## tabla de dimencion "Location"
    Location = df_Taxi_zone.copy()

    to_str = lambda x: str(x)
    taxi_trip_2018['Travel_time'] = taxi_trip_2018['Travel_time'].apply(to_str)

    #normalizo la columna "Date" del "calendario" con la forma "AAAA-MM-DD"
    #calendar["Date"] = pd.to_datetime(calendar["date"])
    # renombro columna id de "calendario"
    #calendar.rename(columns={'id':'IdCalendar'}, inplace=True)
    # organizo las columnas 
    #calendar = calendar.reindex(columns=['IdCalendar','Date','year','week','day','hour'])

    # TODO: Logs
    log('TRANSFORM TRIPS DATA SUCCESSFULY.')
    log('TRANSFORM VENDORS DATA SUCCESSFULY.')
    log('TRANSFORM RATECODE DATA SUCCESSFULY.')
    log('TRANSFORM PAYMENT DATA SUCCESSFULY.')
    log('TRANSFORM BOROUGH DATA SUCCESSFULY.')
    log('TRANSFORM LOCATION DATA SUCCESSFULY.')
    #print(f'\n[{str(dt.now())[:19]}] - TRANSFORM CALENDAR DATA SUCCESSFULY.')



    # TODO: Agregar calendario cuando se pueda
    lista_table=[Borough, Location,Ratecode,payment,vendor, taxi_trip_2018] 

    return lista_table
