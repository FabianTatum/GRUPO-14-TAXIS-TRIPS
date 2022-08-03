#!/home/fabiantatum/miniconda3/envs/dash-plotly python3

from urllib.request import urlopen
import db
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from logs import log
from pandarallel import pandarallel
from datetime import datetime as dt
from numpy import log as ln

def distribution_trips_hour():
    df = db.conn(
    '''
    SELECT *
    FROM taxi_trips;
    '''
    )

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    mask_dia = np.zeros((df.tpep_pickup_datetime.shape[0], 1))
    for idx, i in enumerate(df.tpep_pickup_datetime):
        mask_dia[idx] =  str(i.strftime("%d"))#+"-"+i.strftime("%H")
        
    mask_dia = mask_dia.sum(axis=1)
    df['dia_hora'] = mask_dia
    df.dia_hora = df.dia_hora.astype('str')

    mask_hora = np.zeros((df.tpep_pickup_datetime.shape[0], 1))
    for idx, i in enumerate(df.tpep_pickup_datetime):
        mask_hora[idx] =  i.strftime("%H")
        
    mask_hora = mask_hora.sum(axis=1)
    df['hora'] = mask_hora
    df['dia'] = mask_dia
    df.hora = df.hora.astype('int')

    df.dia_hora = df.dia_hora + '-' + df.hora.astype('str')

    d = pd.DataFrame((df.groupby(['dia_hora','hora']).size()))
    statistics = pd.DataFrame(d.values, columns=['viajes_amount'])

    horas = np.zeros((d.values.shape[0],1))
    for idx, i in enumerate(d.index):
        horas[idx] = i[1]

    statistics['hora'] = horas

    f = statistics.hora.unique()

    boxes = list(range(0,24))
    h = f[[3, 1, 5, 6, 4, 0, 2]]

    for i in boxes:
        boxes[i] = np.array(statistics.viajes_amount[statistics.hora == f[i]])

    f = statistics.hora.unique()
    f = np.sort(f)
    boxes = list(range(0,24))

    for i in boxes:
        boxes[i] = np.array(statistics.viajes_amount[statistics.hora == f[i]])

    f = f.astype('int')
    f = f.astype('str')

    fig = go.Figure()
    for idx, i in enumerate(boxes):
        fig.add_trace(go.Box(y=i, name=f[idx],
                    marker_color='rgb(214, 214, 44)', 
                    opacity=0.8
                    ))

    fig.update_layout(title_text='Distribución de Viajes por Hora')

    return fig

def distribution_trips_day():

    def week_day(param):
        import datetime
        return param.strftime("%A")

    def weekOfyear(param):
        import datetime
        return param.strftime("%W")

    df1 = db.conn(
        ''' 
        SELECT tpep_pickup_datetime
        FROM taxi_trips;
        '''
    )

    df = df1[['tpep_pickup_datetime']].copy()
    del df1

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df['WeekDay'] = df.tpep_pickup_datetime
    df['YearWeek'] = df.tpep_pickup_datetime

    pandarallel.initialize(progress_bar=False)

    df.WeekDay = df.WeekDay.parallel_apply(week_day)
    df.YearWeek = df.YearWeek.parallel_apply(weekOfyear)

    z = pd.DataFrame((df.groupby(['WeekDay','YearWeek']).size()))
    statistics = pd.DataFrame(z.values, columns=['viajes_amount'])

    day = list(range(0,z.values.shape[0]))
    for idx, i in enumerate(z.index):
        day[idx] = i[0]

    statistics['DayWeek'] = day

    f = statistics.DayWeek.unique()

    boxes = list(range(0,7))
    h = f[[3, 1, 5, 6, 4, 0, 2]]

    for i in boxes:
        boxes[i] = np.array(statistics.viajes_amount[statistics.DayWeek == h[i]])

    fig = go.Figure()
    for idx, i in enumerate(boxes):
        fig.add_trace(go.Box(y=i, name=h[idx],
                    marker_color='rgb(214, 214, 44)', 
                    opacity=0.8
                    ))

    fig.update_layout(title_text='Distribución de Viajes por Día')


    return fig


def median_trips_day():

    def week_day(param):
        import datetime
        return param.strftime("%A")

    def weekOfyear(param):
        import datetime
        return param.strftime("%W")

    df1 = db.conn(
        '''
        select *
        from taxi_trips;
        '''
    )
    df = df1[['tpep_pickup_datetime']].copy()

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df['WeekDay'] = df.tpep_pickup_datetime
    df['YearWeek'] = df.tpep_pickup_datetime

    pandarallel.initialize(progress_bar=False)

    df.WeekDay = df.WeekDay.parallel_apply(week_day)
    df.YearWeek = df.YearWeek.parallel_apply(weekOfyear)

    z = pd.DataFrame((df.groupby(['WeekDay','YearWeek']).size()))
    statistics = pd.DataFrame(z.values, columns=['viajes_amount'])

    # get index from statistics
    day = list(range(0,z.values.shape[0]))
    for idx, i in enumerate(z.index):
        day[idx] = i[0]

    statistics['DayWeek'] = day


    f=statistics.DayWeek.unique()
    days = f[[3, 1, 5, 6, 4, 0, 2]]
    y0 = statistics.groupby('DayWeek').median().viajes_amount
    y0 = y0[[3, 1, 5, 6, 4, 0, 2]]

    fig = go.Figure([go.Bar(x=days, y = y0)])

    # Customize aspect
    fig.update_traces(marker_color='rgb(238, 238, 27)', 
                    marker_line_color='rgb(187, 187, 50)',
                    marker_line_width=1.5, 
                    opacity=0.6)

    fig.update_layout(title_text='Media de Viajes por Día')

    return fig, df1
    


def borough_map(intro='fare_amount'):
    nyc_geojson = './assets/borough_nyc.geojson'
    nyc_boroughs = json.load(open(nyc_geojson))
    table = db.conn(
        '''
        SELECT b.borough, t.fare_amount, t.total_amount_1
        from taxi_trips as t
        inner join borough as b
        on t.idborough = b.idborough;
        '''
    )
    log('Consulta realizada.')

    resume = table.groupby(by=['borough'], as_index=False).sum()
    log('Agrupamiento hecho')


    borough_map = {}
    for feature in nyc_boroughs['features']:
        feature['id'] = feature['properties']['boro_code']
        borough_map[feature['properties']['boro_name']] = feature['id']

    borough_id = pd.Series(borough_map)
    borough_id = pd.DataFrame(borough_id)
    borough_id.reset_index(inplace=True)
    borough_id.rename(columns={'index': 'borough', 0:'id_borough'}, inplace=True)

    df = pd.merge(resume, borough_id, how='left')
    df.drop(labels=[5], inplace=True)

#40.730610, and the longitude is -73.935242
    log('Grafico Mapbox Iniciado...')
    fig = px.choropleth_mapbox(df, geojson=nyc_boroughs, color=intro,
                            locations="id_borough", featureidkey="id",
                            center={"lat": 40.730610, "lon": -73.935242},
                            mapbox_style="carto-positron", zoom=9, opacity=0.4,
                            hover_name='borough')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    log('Grafico construido.')
    return fig

def borough_map_pop():

    taxi_trip_2018 = db.conn(
        '''
            select * from taxi_trips;
        ''' 
        
    )

    Borough = db.conn(
        '''
            select * from borough;
        ''' 
        
    )

    Location = db.conn(
        '''
            select * from location;
        ''' 
        
    )

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    d = ['36005', '36047', '36061', '36081', '36085']
    name = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens',  'Staten Island']

    c = pd.DataFrame()
    c['fips'] = d
    c['borough'] = name
    c['unemp'] = [1,3,6,8,11]

    directorio_Location = '../in/taxi_zone_lookup.csv'

    df_Taxi_zone = pd.read_csv(directorio_Location)

    def algo(params):
        if params == 'EWR':
            return 1
        if params == 'Queens':
            return 2
        if params == 'Bronx':
            return 3
        if params == 'Manhattan':
            return 4
        if params == 'Staten Island':
            return 5
        if params == 'Brooklyn':
            return 6
        else:
            return params
    print('3/4')

    pandarallel.initialize()
    # subescribo los valores del df "df_Taxi_zone" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
    df_Taxi_zone.Borough = df_Taxi_zone.Borough.parallel_apply(algo)
    # renombro la columna 
    df_Taxi_zone.rename(columns={'Borough':'IdBorough'}, inplace=True)
    # realizo un drop de la columna "service_zone"
    #df_Taxi_zone.drop('service_zone',axis=1 ,inplace=True)
    # tabla de dimencion "Location"
    Location = df_Taxi_zone.copy()
    #normalizo la columna "Date" del "calendario" con la forma "AAAA-MM-DD"
    #calendar["Date"] = pd.to_datetime(calendar["date"])
    # renombro columna id de "calendario"
    #calendar.rename(columns={'id':'IdCalendar'}, inplace=True)
    # organizo las columnas 
    #calendar = calendar.reindex(columns=['IdCalendar','Date','year','week','day','hour'])
    # Funcion para relacionar los indices de una columna con otra para la tabla taxi_trip_2018
    #def algo1(params):
    #    try:
    #        return Borough.IdBorough[Borough.Borough== params].iloc[0]
    #    except:
    #        return 7
    # subescribo los valores del df "taxi_trip_2018" de la columna "borough" y le aplico un nuevo valores con la funcion creada arriba
    #taxi_trip_2018.IdBorough = taxi_trip_2018.idBorough.parallel_apply(algo)     #1)----------------------------------------------
    # Cambio el nombre de la columna "Borough" 
    taxi_trip_2018.rename(columns={'Borough':'IdBorough'}, inplace=True)

    #lista_table=[Borough, Location,Ratecode,payment,vendor, calendar, taxi_trip_2018] 
    lista_table = []
    lista_table.append(taxi_trip_2018)
    #print(type(lista_table))
    #print(type(lista_table[0]))
    #print(lista_table[0].head())
    print('4/4')

    Borough.rename(columns={'idborough':'IdBorough'}, inplace=True)

    df_Taxi_zone = df_Taxi_zone.merge(Borough, how= 'left', on='IdBorough')
    df_Taxi_zone.drop(columns=['Zone','latitude', 'longitude'], inplace=True)


    df_Taxi_zone.loc[df_Taxi_zone[df_Taxi_zone.IdBorough == 'Unknown'].index,'borough'] = 'Unknown'

    # marge DropOff location
    taxi_trip_2018 = taxi_trip_2018.merge(df_Taxi_zone, how = 'left', right_on = 'LocationID', left_on = 'idpulocation')
    #taxi_trip_2018.drop(columns= ['IdPULocation', 'LocationID'], inplace=True)
    taxi_trip_2018.rename(columns={'Borough' : 'boroughPU'}, inplace=True)

    # marge entre columnas bla bla bla
    taxi_trip_2018 = taxi_trip_2018.merge(df_Taxi_zone, how = 'left', right_on = 'LocationID', left_on = 'iddolocation')
    #taxi_trip_2018.drop(columns= ['IdDOLocation', 'LocationID'], inplace=True)
    taxi_trip_2018.rename(columns={'Borough':'boroughDO'}, inplace=True)

    z = (taxi_trip_2018.groupby(['borough_x', 'borough_y']).size()).unstack()

    z.sum()

    z.fillna(0, inplace=True)
    z.drop(columns=['EWR'], inplace=True)
    z.drop(['EWR'], axis=0, inplace=True)
    z.drop(columns=['Unknown'], axis=1 , inplace = True)
    z.drop(['Unknown'], axis=0, inplace=True)

    c.unemp = z.sum().values
    c.loc[:,'unemp'] = ln(c.unemp)

    fig = px.choropleth_mapbox(c, geojson=counties, locations='fips', color='unemp',
                            color_continuous_scale=px.colors.sequential.YlOrBr,
                            range_color=(0, c.unemp.max()),
                            mapbox_style="carto-positron",
                            zoom=9,
                            center= {"lat": 40.7080747, "lon": -73.9810613},
                            opacity=0.5,
                            labels={'unemp':'trips scale'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


