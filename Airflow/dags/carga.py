import pandas as pd
from sqlalchemy import create_engine


def ingest_callable(user, password, host, port, db, table_name, list_frames, execution_date):
    #print(table_name, list_frames, execution_date)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
#
    print('connection established successfully, inserting data...')
#
#
    for idx, tabla in enumerate(list_frames):
        #CREAR TABLA IF EXIST IGNORE
        try:
            tabla.head(n=0).to_sql(name=table_name[idx], con=engine, index=False)
        except:
            print('Tabla existente')

        # INSERTAR DATOS EN TABLA
        tabla.to_sql(name=table_name[idx], con=engine, if_exists='append', index=False, chunksize=1000000)
    
    engine.connect().close()