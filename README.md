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

<center>![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/distribucion_viaje_dia.png?raw=true)</center>

En la siguiente gráfica se observa, como se espera, una tendencia creciente en cuanto al numero de viajes conforme se aproximan los horarios de entrada y salida laboral , aunque de forma muy variable, es decir, a dichas horas se pueden efectuar muchos o pocos viajes.
Luego, durante el período de 10hs a 16hs se requiere un número ciertamente acotado entre 10.000 y 17.000 viajes. Al aproximarse el horario de fin de jornada (17hs ~ 19hs) se observan los valores más elevados, llegando a efectuarse hasta 21.000 viajes por hora. Luego, conforme continúa el día la cantidad de viajes efectuados decrece hasta el próximo día a las 06hs.
  
<center>![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/dist_viaje_hora.png?raw=true)</center>

Como se observa en el gráfico, más del 90% de los viajes de taxi se realizan en la zona de Manhattan. Distribuyendose el resto de los viajes entre Brooklyn y Queens. Para el espacio muestreado, no se observan practicamente viajes en el borough de  Staten Island.

![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/map_popu_borough.png?raw=true)

## Regresión lineal 

En esta sección creamos un algoritmo de regresión lineal, buscando el coeficiente de correlación entre las variables monto y distancia. El objetivo es, dada una distancia de viaje, predecir el monto aproximado de viaje, de modo que el cliente sepa de ante mano cuánto le puede costar. 

Para este modelo se utilizó la librería Scikit-learn, una librería de aprendizaje automático de código abierto para python. Se tomaron como datos los pertenecientes a Enero-2018 y se realizó una partición de los datos para train/test en una proporción de 0.75/0.25 con una limpieza previa de valores atípicos para mejorar la eficacia del modelo. 

![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/regresion_dist_monto_total.png?raw=true)

Como se puede ver, la regresión retorna una recta de valor $ y = 3.5548\cdot x + 5.4629$

## Análisis de Serie de Tiempo

Para realizar el análisis de serie de tiempo se tomaron datos de la demanda de taxis en la ciudad de Nueva York desde el 1 de junio del 2017 hasta el 31 de enero del 2018. De la totalidad de viajes registrados durante los 8 meses bajo análisis se obtuvo un muestreo aleatorio estratificado, segmentando los datos por días e incluyendo el 12.5% de los valores de cada día en la muestra. De esta manera, se logró reducir considerablemente la cantidad de datos sin perder la frecuencia diaria.

Una vez obtenida la muestra, se realizó un análisis de outliers detectando ciertos valores que se alejaban de la muestra en forma excesiva y distorsionaban el análisis. Realizando un análisis más detallado se pudo observar que estos valores coinciden con días en donde el servicio de taxis no funciono de manera habitual, resultando en contadores extremadamente bajos. Se eliminaron los valores clasificados como outliers para un mejor fiiting del modelo.

Se utilizo Meta Prophet para llevar a cabo la predicción, una biblioteca de código abierto desarrollada por Facebook (Meta) para el análisis de series temporales. Prophet lleva a cabo un procedimiento para pronosticar datos de series temporales basado en un modelo aditivo en el que las tendencias no lineales se ajustan a la estacionalidad anual, semanal y diaria. Es adecuada para trabajar con series temporales que tienen fuertes efectos estacionales, como es el caso de los taxis de NYC, donde se observan cambios en la demanda según el día de la semana. Es resistente a datos faltantes y cambios de tendencia, y por lo general maneja bien valores atípicos. 

El modelo TSF de Prophet segrega la serie de tiempo predicha en 2 componentes. Un primer componente de tendencia general donde observamos una directriz bajista que ronda el nivel de 32.000 viajes diarios y un segundo componente de estacionalidad semanal, el cual indica que la demanda de taxis crece a medida que se acerca el fin de semana, siendo el domingo el día con menor demanda. 


![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/season.jpg?raw=true)

Al combinar el componente de tendencia y el estacional, el resultado es una predicción de la demanda futura de taxis para un mes el próximo a la fecha de análisis. El pronóstico generado mediante Prophet es una onda de tipo sinusoidal que oscila entre los valores 27.800 y 35.000 indicando que la demanda para el mes de febrero se ubicará entre tales valores. 

![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/TSF%20final.PNG?raw=true)

Podemos medir la eficacia del modelo a través del MAPE. El Error Porcentual Absoluto Medio (MAPE o Mean Absolute Percentage Error) es un indicador del desempeño del Pronóstico de Demanda que mide el tamaño del error (absoluto) en términos porcentuales. El MAPE promedio del modelo confeccionado es del 11.17% lo cual indica que la diferencia promedio entre el valor pronosticado por el modelo y el valor real es del 11.17%. Un MAPE entre 10 % y 25 % indica una precisión aceptable para un modelo de demanda. 

![alt text](https://github.com/facundoallia/Analisis-NYC-Taxis/blob/main/assets/MAPE.jpg?raw=true)
