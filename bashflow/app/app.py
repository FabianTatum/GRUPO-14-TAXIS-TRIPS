from dash import Dash, html, dcc, Input, Output
import figures

################################
#------------ DATOS -----------#
################################

################################
#----------GRAFICAS -----------#
################################
boroughs_map_intro_fig = figures.borough_map(intro='borough')
boroughs_map_fig = figures.borough_map()
median_trips_day_fig = figures.median_trips_day()
distribution_trips_day_fig = figures.distribution_trips_day()
distribution_trips_hour_fig = figures.distribution_trips_hour()

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
                        INTRODUCCION
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
                            'hipervinculo'
                        ]),

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
                        'Mapa de Nueva York'
                    ], className='section-title'),
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

                html.H2(children=[
                    "Ingresa el valor para tu predicción",
                ],
                ),

                html.Div(children=[

                    dcc.Input(id='my-input', value='', type='float')

                ], style={'display': 'block'}
                ),

            ], className='hero-image-opacity',
            ),

            html.P(
            id='my-output',
            className='paragraph-text',
            style={'textAlign': 'center'}
            ),

        ], className='hero-image',
        style={'backgroundColor': 'var(--white-alpha-color)'}
        ),

    ], className='section bg-gray-light',
    style={'backgroundImage': 'url(assets/streets-background2.jpg)', 'backgroundAttachment': 'fixed'}
    ),

])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'El valor del viaje es ${input_value}'

################################
#--------BODY DE LA APP--------#
################################
if __name__ == '__main__':
    app.run_server(debug=False)
