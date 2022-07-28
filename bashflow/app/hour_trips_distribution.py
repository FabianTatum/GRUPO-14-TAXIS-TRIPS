#!/usr/bin/env python
# coding: utf-8

import db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandarallel import pandarallel
import plotly.graph_objects as go

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
                marker_color = 'blue'))

fig.update_layout(
    autosize=False,
    width=800,
    height=500,
    font_color="blue",
#    title = 'Distribucion de viajes por hora',
#    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size = 50
    )

fig.show()

