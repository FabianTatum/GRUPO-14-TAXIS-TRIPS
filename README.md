# Análisis NYC Taxis

El objetivo de este proyecto es  brindar un análisis tanto cuantitativo como  cualitativo acerca de los movimientos diarios de taxis en la ciudad de Nueva York y su relación con distintas variables como el clima o el horario. El objetivo del análisis es brindar un  mejor entendimiento y sustento en la toma de decisiones para futuros conductores y/o propietarios de empresas que quieran ingresar al sector. Dado que la ciudad de Nueva York es de las más pobladas a nivel mundial, mensualmente se toman millones de taxis.

## KPI - Key Performance Indicators

Se busca evaluar el comportamiento de la demanda mediante el análisis de las características inherentes a cada viaje en taxi. Se evaluarán las relaciones entre dichas características tales como: 

| KPI             | Métrica    
|-------------------|-------------|
| Medir horas más demandados del día | AVG viajes/hora |
| Medir días más demandados | AVG viajes/día de la semana |
| Medir variaciones de demanda en el tiempo | Variación de Cantidad de viajes |
| Medir orígenes y destinos más demandados | Suma viajes con destino a cada borough |
| Evaluar montos de viajes según distancia | Monto $ /Distancia Monto $/Tiempo |

## Análisis de KPIs

La gráfica de la distribución de la cantidad de viajes respecto a los días de la semana nos dice que no hay gran variación entre ellos, y tal como se esperaba la demanda crece a medida que se acerca el fin de semana, siendo el domingo elde menor valor. A su vez, tambien se ve que el jueves es el tiene y siempre en un rango más acotado, el 50% de los jueves analizados tuvieron entre 38000 y 42800 viajes.

![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/distribucion_viaje_dia.png?raw=true)

En la siguiente gráfica se observa, como se espera, una tendencia creciente en cuanto al numero de viajes conforme se aproximan los horarios de entrada y salida laboral , aunque de forma muy variable, es decir, a dichas horas se pueden efectuar muchos o pocos viajes.
Luego, durante el período de 10hs a 16hs se requiere un número ciertamente acotado entre 10.000 y 17.000 viajes. Al aproximarse el horario de fin de jornada (17hs ~ 19hs) se observan los valores más elevados, llegando a efectuarse hasta 21.000 viajes por hora. Luego, conforme continúa el día la cantidad de viajes efectuados decrece hasta el próximo día a las 06hs.

Como se observa en el gráfico, más del 90% de los viajes de taxi se realizan en la zona de Manhattan. Distribuyendose el resto de los viajes entre Brooklyn y Queens. Para el espacio muestreado, no se observan practicamente viajes en el borough de  Staten Island.

## Análisis de Serie de Tiempo

Para realizar el análisis de serie de tiempo se tomo un muestreo aleatorio estratificado de los datos de demanda de taxis en la ciudad de Nueva York desde el 1 de junio del 2017 hasta el 31 de enero del 2018.  el resultado es una predicción de la demanda futura de taxis para un mes el próximo a la fecha de análisis. El pronóstico generado mediante Prophet es una onda de tipo sinusoidal que oscila entre los valores 27.800 y 35.000 indicando que la demanda para el mes de febrero se ubicará entre tales valores.
