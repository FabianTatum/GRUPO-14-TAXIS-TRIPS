#!/usr/bin/env python

import db
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from logs import log

def linear_regression_pred(value):

    taxi_api = db.conn(
        '''
            select * from taxi_trips;
        ''' 
    )

    # TODO: Analisis
    # parte de abajo
    taxi_api.drop(taxi_api[taxi_api['trip_distance'] == 0.0].index, inplace = True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >= 0) & (taxi_api['total_amount_1']<=3)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >=0.7 ) & (taxi_api['total_amount_1']<=4 )].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >=0.8 ) & (taxi_api['total_amount_1']<=4.3 )].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >=1) & (taxi_api['total_amount_1']<=4.4 )].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >=1.3) & (taxi_api['total_amount_1']<=5 )].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >= 1.5) & (taxi_api['total_amount_1']<=5.3)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >= 2) & (taxi_api['total_amount_1']<=7)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >= 2.3) & (taxi_api['total_amount_1']<=7.3)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >= 3) & (taxi_api['total_amount_1']<=8.5)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] >= 3.5) & (taxi_api['total_amount_1']<=9)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] > 0) & (taxi_api['total_amount_1']>=40)].index, inplace=True)
    # parte de arriba
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] < 1) & (taxi_api['total_amount_1']>=25)].index, inplace=True)
    taxi_api.drop(taxi_api[(taxi_api['trip_distance'] < 3.5) & (taxi_api['total_amount_1']>=34)].index, inplace=True)

    X_train, X_test, y_train, y_test= train_test_split(taxi_api.trip_distance,taxi_api.total_amount_1 , test_size=0.33, random_state=42)

    lr=LinearRegression()
    lr.fit(X_train.values.reshape(-1,1),y_train.values)

#    prediction=lr.predict(X_test.values.reshape(-1,1))
    print('pendiente:', lr.coef_)
    print('----------------------------------')
    print('interseccion:', lr.intercept_)

    log('Entrada a predecir el valor')

    def price(param):
        log(f'Value in func price: {param}')
        log(f'Type in func price: {type(param)}')
        valor = lr.predict(np.array([[param]]))[0]
        return valor

    log('predicion hecha...')
    
    return round(price(value), 2)



#fig = px.scatter(
#    taxi_api, x=X_test, y=y_test, opacity=0.65,
#    trendline='ols', trendline_color_override='darkblue'
#)
#fig.show()


# ### recordar: un notebook por cada grafica y analisis
