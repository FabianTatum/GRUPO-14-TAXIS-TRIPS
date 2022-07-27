import pandas as pd
import re
import numpy as np
import datetime

# indice en la muestra
def random_sample(df, date):

    # crear dataframe vacio para el sample
    muestra = pd.DataFrame()
    # Creamos las columnas del dataframe
    for i in df:
        muestra[i] = i

    # CODIGO PARA CREAR SAMPLES DE LOS N ARCHIVOS

        
        # --------------------CODIGO NECESARIO PARA CREAR EL SAMPLE---------------------------
    #date = re.findall(r'\S*([0-9][0-9][0-9][0-9]-[0-9][0-9]).parquet', file)
    
    # Directorio para los archivos
    #ruta = 'datasets/taxi_trip/yellow_tripdata_'+date[0]+'.parquet'
#-----------------------------------------------------------------------------------------------------
    # Obtener cota de los meses
    final_date = date+'-01'
    date = date.split('-')
    execution_date = datetime.datetime(int(date[0]), int(date[1]), 1)
    final_date = execution_date + datetime.timedelta(days = pd.Period(final_date).days_in_month )
#-----------------------------------------------------------------------------------------------------

    # Cargamos dataset
    #df = pd.read_parquet(ruta)
#-----------------------------------------------------------------------------------------------------

    # eliminamos registros con fechas diferentes al mes en cuestion con base en la cota de los meses
    df.drop(df[df['tpep_pickup_datetime'] > final_date].index, inplace = True)
    df.drop(df[df['tpep_pickup_datetime'] < execution_date].index, inplace = True)
#-----------------------------------------------------------------------------------------------------

    # creamos la mask para un dia y la hora
    mask_dia = np.zeros((df.tpep_pickup_datetime.shape[0], 1))
    mask_hora = np.zeros((df.tpep_pickup_datetime.shape[0], 1))

    for idx, i in enumerate(df.tpep_pickup_datetime):
        mask_dia[idx] =  i.strftime("%d")
    
    for idx, i in enumerate(df.tpep_pickup_datetime):
        mask_hora[idx] =  i.strftime("%H")
#-----------------------------------------------------------------------------------------------------

    # Creamos los arrays en los que vamos a iterar
    dias = np.unique(mask_dia)
    horas = np.unique(mask_hora)
#-----------------------------------------------------------------------------------------------------

    # Ajustamos las mascaras para poder usarlas
    mask_dia = mask_dia.sum(axis=1)
    mask_hora = mask_hora.sum(axis=1)
#-----------------------------------------------------------------------------------------------------

    # Obtenemos la muestra
    for d in dias:
        for h in horas:    
            # dataframe filtrando por dia y hora
            aux = df[(mask_dia == d) & (mask_hora == h)]
    
            # obtenemos la muestra aleatoria del 12.5% de los datos
            mu = aux.sample(frac =.125)
    
            # Concatenamos mu con la muestra
            muestra = muestra.append(mu)
            del mu
            del aux
        #print('Dia '+str(d)+' finalizado')
    return muestra
    