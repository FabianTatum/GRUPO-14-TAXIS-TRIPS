import pandas as pd

def initial_tables():
    ## CREACION TABLAS DE DIMENCION TAXI TRIP
    vendor={    1:'Creative Mobile Technologies, LLC',
                2:'VeriFone Inc'}
    vendor = pd.DataFrame([[key, vendor[key]] for key in vendor.keys()], columns=['IdVendor', 'Name_vendor'])
    #--------------------------------------------------------------------------------
    Ratecode={  1:'Tarifa estándar',
                2:'jfk',
                3:'nuevaark',
                4:'nassau o westchester',
                5:'tarifa negociada',
                6:'paseo en grupo'}
    Ratecode = pd.DataFrame([[key, Ratecode[key]] for key in Ratecode.keys()], columns=['IdRatecode', 'Name_ratecode'])
    #--------------------------------------------------------------------------------

    payment={   1:'tarjeta de crédito',
                2:'efectivo',
                3:'sin cargo',
                4:'disputa',
                5:'desconocido',
                6:'viaje anulado'}
    payment = pd.DataFrame([[key, payment[key]] for key in payment.keys()], columns=['IdPayment_type', 'Payment_type'])
    #--------------------------------------------------------------------------------

    Borough_dic = [ {'IdBorough':1,'Borough':'EWR','Latitude':40.6895314,'Longitude':-74.17446239999998},
                    {'IdBorough':2,'Borough':'Queens','Latitude':40.742054,'Longitude':-73.769417},
                    {'IdBorough':3,'Borough':'Bronx','Latitude':40.837048,'Longitude':-73.865433},
                    {'IdBorough':4,'Borough':'Manhattan','Latitude':40.776676,'Longitude':-73.971321},
                    {'IdBorough':4,'Borough':'Staten Island','Latitude':40.579021,'Longitude':-74.151535},
                    {'IdBorough':6,'Borough':'Brooklyn','Latitude':40.650002,'Longitude':-73.949997}]
    Borough = pd.DataFrame(Borough_dic)
    #--------------------------------------------------------------------------------

    df_Taxi_zone = pd.read_csv('logs/taxi_zone_lookup.csv')
    # Reemplazo valores nulos
    df_Taxi_zone['Zone'].fillna('Not specified',inplace=True)
    df_Taxi_zone['service_zone'].fillna('Not specified',inplace=True)

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
    #Location = df_Taxi_zone.copy()
    #--------------------------------------------------------------------------------

    calendar = pd.read_csv('logs/calendar.csv', sep=';')
    #normalizo la columna "Date" del "calendario" con la forma "AAAA-MM-DD"
    calendar["Date"] = pd.to_datetime(calendar["date"])
    # renombro columna id de "calendario"
    calendar.rename(columns={'id':'IdCalendar'}, inplace=True)
    # organizo las columnas 
    calendar = calendar.reindex(columns=['IdCalendar','Date','year','week','day','hour'])
    #--------------------------------------------------------------------------------

    ## Creacion de tablas de DIMENSION WEATHER

    icon ={
        0: 'night',
        1: 'day'}
    icon = pd.DataFrame([[key, icon[key]] for key in icon.keys()], columns=['Idcondicion', 'condicion'])
    # -------------------------------------------------------------------------------

    cond = pd.read_csv('logs/conditions_weather.csv')
    cond = cond.reset_index()
    cond.rename(columns={'index':'id_condition','id':'key_api'}, inplace=True)

    list_tables = [vendor,Ratecode,payment,Borough, df_Taxi_zone, calendar, icon, cond]
    name_tables = ['vendor','ratecode','payment','borough', 'location', 'calendar', 'icon', 'condition']

    return name_tables, list_tables


