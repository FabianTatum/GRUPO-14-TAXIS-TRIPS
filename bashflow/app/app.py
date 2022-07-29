from dash import Dash, html, dcc, Input, Output
import figures
import linear_regression as lr_pred
from logs import log

################################
#------------ DATOS -----------#
################################

################################
#----------GRAFICAS -----------#
################################
boroughs_map_intro_fig = figures.borough_map(intro='borough')
boroughs_map_fig = figures.borough_map_pop()
median_trips_day_fig = figures.median_trips_day()
distribution_trips_day_fig = figures.distribution_trips_day()
distribution_trips_hour_fig = figures.distribution_trips_hour()

#reference
median_trips_day_fig_ref = figures.median_trips_day()
distribution_trips_day_ref = figures.distribution_trips_day()

################################
#--------BODY DE LA APP--------#
################################

external_stylesheets = [
        'https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap',
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[

# TODO: Header de la app
    html.Header(children=[
        html.Section(children=[
            html.Div([
                html.A(children='TLC NEW YORK')
            ], className='logo')
        ], className='container')
    ],className='header'),

# TODO: Imagen de presentacion
    html.Section(children=[
        html.Article(children=[
            html.Aside(children=[
                html.Div(children=[
                    html.H2(children=[
                        '¿Quieres conocer el negocio de los taxis en la gran manzana?',
                        html.Br(children=[]),
                        html.Br(children=[]),
                        'Este es el lugar'
                    ],
                    className='hero-image-title',
                    style={'color': 'var(--first-alpha-color)'}
                    )
                ], className='hero-image-content')
            ], className='hero-image-opacity',
            style={'backgroundColor': 'var(--black-alpha-color)'}
            )
        ], className='hero-image',
        style={'backgroundImage': 'url(assets/hero-image-home.jpg)', 'backgroundAttachment': 'fixed'}
        )
    ], className='home'),


    html.Section(children=[

        html.Article(children=[

            html.Aside(children=[

                html.Div(children=[

                    html.H2(children=[
                        'INTRODUCCIÓN'
                    ], className='section-title'),

                    html.P(children=[
                        '''
                        El objetivo de este proyecto es  brindar un análisis tanto cuantitativo como 
                        cualitativo acerca de los movimientos diarios de taxis en la ciudad de Nueva York 
                        y su relación con distintas variables como el clima o el horario. El objetivo del 
                        análisis es brindar un  mejor entendimiento y sustento en la toma de decisiones para 
                        futuros conductores y/o propietarios de empresas que quieran ingresar al sector. 
                        Dado que la ciudad de Nueva York es de las más pobladas a nivel mundial, mensualmente 
                        se toman millones de taxis. El registro de estos movimientos se encuentra disponible en 
                        su pagina 
                        ''',

                        html.A(children=[
                            'TLC Trip Record Data.'
                        ], href='https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page'),

                    ], className='paragraph-text'
                    ),

                    html.Div(children=[

                        dcc.Graph(
                            id='map_boroughs_intro',
                            figure=boroughs_map_intro_fig
                        ),

                    ]),

                ], className='container full-lg-screen',
                )

            ], className='hero-image-opacity',
            ),

        ], className='hero-image',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),


    html.Section(children=[

        html.Div(children=[

            html.Article(children=[

                html.H2(children=[
                    'Media de viajes por dia'
                ], className='section-title'),

                html.P(children=[
                    '''
                    La gráfica de la distribución de la cantidad de viajes respecto 
                    a los días de la semana nos dice que no hay gran variación entre ellos, 
                    y tal como se esperaba la demanda crece a medida que se acerca el fin de semana, 
                    siendo el domingo elde menor valor.
                    '''
                ], className='paragraph-text'
                )

            ], className='service-card',
            ),

            html.Article(children=[

                dcc.Graph(
                    id='median_fig',
                    figure=median_trips_day_fig
                ),

            ], className='service-card',
            ),

            html.Article(children=[

                dcc.Graph(
                    id='distribution_fig',
                    figure=distribution_trips_day_fig
                ),

            ], className='service-card'
            ),

            html.Article(children=[

                html.H2(children=[
                    'Distribución de viajes por dia'
                ], className='section-title'),

                html.P(children=[
                    '''
                    A su vez, tambien se ve que el jueves es el tiene y siempre en un rango más acotado, 
                    el 50% de los jueves analizados tuvieron entre 38000 y 42800 viajes.
                    '''
                ], className='paragraph-text'
                )

            ], className='service-card',
            ),



        ], className='container full-lg-screen',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='services section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),


    html.Section(children=[

        html.Article(children=[

            html.Aside(children=[

                html.Div(children=[
                    
                    html.H2(children=[
                        'Distribución por horas'
                    ], className='section-title'),

                    html.P(children=[
                        '''
                        En la siguiente gráfica se observa, como se espera, una tendencia creciente 
                        en cuanto al numero de viajes conforme se aproximan los horarios de entrada y 
                        salida laboral , aunque de forma muy variable, es decir, a dichas horas se pueden 
                        efectuar muchos o pocos viajes. ''',
                        html.Br(),
                        '''
                        Luego, durante el período de 10hs a 16hs se requiere un número ciertamente acotado 
                        entre 10.000 y 17.000 viajes. Al aproximarse el horario de fin de jornada (17hs ~ 19hs)
                        se observan los valores más elevados, llegando a efectuarse hasta 21.000 viajes por hora. 
                        Luego, conforme continúa el día la cantidad de viajes efectuados decrece hasta el próximo día 
                        a las 06hs.
                        '''
                    ], className='paragraph-text'
                    ),

                    html.Div(children=[
                        dcc.Graph(
                            id='hour_distribution',
                            figure=distribution_trips_hour_fig
                        ),
                    ]),
                ], className='container full-lg-screen',
                )

            ], className='hero-image-opacity',
            ),

        ], className='hero-image',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),

    html.Section(children=[


        html.Article(children=[

            html.Aside(children=[

                html.Div(children=[

                    html.H2(children=[
                        'Análisis geográfico de la cantidad de viajes por borough'
                    ], className='section-title'),

                    html.P(children=[
                        '''
                        Como se observa en el gráfico, más del 90% de los viajes de taxi se realizan 
                        en la zona de Manhattan. Distribuyendose el resto de los viajes entre Brooklyn y Queens. 
                        Para el espacio muestreado, no se observan practicamente viajes en el borough de 
                        Staten Island.
                        '''
                    ], className='paragraph-text'
                    ),

                    html.Div(children=[
                        dcc.Graph(
                            id='map_boroughs',
                            figure=boroughs_map_fig
                        ),
                    ]),
                ], className='container full-lg-screen',
                )

            ], className='hero-image-opacity',
            ),

        ], className='hero-image',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),

    html.Section(children=[

        html.Article(children=[

            html.Aside(children=[

                html.Div(children=[
                    
                    html.H2(children=[
                        'Time Series Prediction'
                    ], className='section-title'),

                    html.P(children=[
                        '''
                        Para realizar el análisis de serie de tiempo se tomo un muestreo aleatorio 
                        estratificado de los datos de demanda de taxis en la ciudad de Nueva York 
                        desde el 1 de junio del 2017 hasta el 31 de enero del 2018.  el resultado es 
                        una predicción de la demanda futura de taxis para un mes el próximo a la fecha 
                        de análisis. El pronóstico generado mediante Prophet es una onda de tipo sinusoidal 
                        que oscila entre los valores 27.800 y 35.000 indicando que la demanda para el mes de 
                        febrero se ubicará entre tales valores.
                        '''
                    ], className='paragraph-text'
                    ),

                    html.Div(children=[

                        html.Img(
                            src='./assets/TSF_final.png',
                            style={'width': '70%', 'height': '70%'}
                        ),

                    ],
                    ),

                ], className='container full-lg-screen',
                )

            ], className='hero-image-opacity',
            ),

        ], className='hero-image',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),


    html.Section(children=[

        html.Div(children=[

            html.Article(children=[

                html.H2(children=[
                    'Linear Regression Prediction'
                ], className='section-title'),

                html.P(children=[
                    '''
                    En esta sección creamos un algoritmo de regresión lineal, buscando el coeficiente de 
                    correlación entre las variables monto y distancia. El objetivo es, dada una distancia 
                    de viaje, predecir el monto aproximado de viaje, de modo que el cliente sepa de ante mano cuánto le puede costar. 
                    Para este modelo se utilizó la librería Scikit-learn, una librería de aprendizaje automático 
                    de código abierto para python. Se tomaron como datos los pertenecientes a Enero-2018 y se 
                    realizó una partición de los datos para train/test en una proporción de 0.75/0.25 con una 
                    limpieza previa de valores atípicos para mejorar la eficacia del modelo. 
                    '''
                ], className='paragraph-text'
                )

            ], className='service-card',
            ),

            html.Article(children=[

                html.Img(
                    src='./assets/lr_image.png',
                    style={'width': '100%', 'height': '100%'}
                ),

            ], className='service-card'
            ),

            html.Article(children=[

                html.H2(children=[
                    "Ingresa la distancia en millas para conocer el monto del viaje:",
                ], 
                style={
                    'margin': '2rem auto',
                    'text-align': 'center',
                    'padding': '0.5rem 1rem',
                    'color': 'var(--title-color)'
                }
                ),

            ], className='service-card',
            ),

            html.Article(children=[

                dcc.Input(id='linear-regression-input', value='0', type='number',
                className='center-block'),

                html.H2(id='linear-regression-output',
                style={
                    'margin': '2rem auto',
                    'text-align': 'center',
                    'padding': '0.5rem 1rem',
                    'color': 'var(--title-color)'
                }
                )

            ], className='service-card'
            ),

        ], className='container full-lg-screen',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='services section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),

    html.Footer(children=[
        html.Small(children=[
            'Repositorio del proyecto ',
            html.A(children=[
                '@Group-14/TLC-Analysis'
            ], href='https://github.com/FabianTatum/GRUPO-14-TAXIS-TRIPS',
            target='_blank'
            ),
        ])
    ], className='footer'
    )

])


@app.callback(
    Output(component_id='linear-regression-output', component_property='children'),
    Input(component_id='linear-regression-input', component_property='value')
)
def update_output_div(input_value):
    if input_value == '' or input_value == None:
        input_value = '0'

    log(f'Input type initial: {type(input_value)}')
    log(f'Input value initial: {input_value}')
        
    value = float(input_value)
    
    log(f'Input type initial: {type(value)}')
    log(f'Input value initial: {value}')

    valor_esperado = lr_pred.linear_regression_pred(value)

    log(f'LR return: {input_value}')

    return f'El valor del viaje es ${valor_esperado}'

################################
#--------BODY DE LA APP--------#
################################
if __name__ == '__main__':
    app.run_server(debug=False)
