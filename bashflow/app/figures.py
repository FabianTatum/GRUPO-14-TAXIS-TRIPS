#!/home/fabiantatum/miniconda3/envs/dash-plotly python3

import db
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from logs import log
from pandarallel import pandarallel
from datetime import datetime as dt

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
    del df1


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

    return fig
    


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

