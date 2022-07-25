import transform as trans
import pandas as pd
from datetime import datetime as dt
import sys

fecha = sys.argv[1]

def load(df_list):

    # Borough
    print(f'[{str(dt.now())[:19]}] - Convert borough DataFrame to csv.')
    df_list[0].to_csv('./out/borough.csv', index=False)


    # Location
    print(f'[{str(dt.now())[:19]}] - Convert location DataFrame to csv.')
    df_list[1].to_csv('./out/location.csv', index=False)

    # Ratecode 
    print(f'[{str(dt.now())[:19]}] - Convert ratecode DataFrame to csv.')
    df_list[2].to_csv('./out/ratecode.csv', index=False)

    # Payment
    print(f'[{str(dt.now())[:19]}] - Convert payment DataFrame to csv.')
    df_list[3].to_csv('./out/payment.csv', index=False)

    # Vendor
    print(f'[{str(dt.now())[:19]}] - Convert vendor DataFrame to csv.')
    df_list[4].to_csv('./out/vendor.csv', index=False)

    # Trips
    print(f'[{str(dt.now())[:19]}] - Convert taxi trips DataFrame to csv.')
    df_list[5].to_csv('./out/taxi_trips.csv', index=False)

df_list = trans.transform(fecha)
load(df_list)

    