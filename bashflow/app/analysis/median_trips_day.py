


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandarallel import pandarallel
import plotly.graph_objects as go
import db


# In[2]:


def week_day(param):
    import datetime
    return param.strftime("%A")

def weekOfyear(param):
    import datetime
    return param.strftime("%W")


# In[3]:


df1 = db.conn(
    '''
    select *
    from taxi_trips;
    '''
)


# In[4]:


df = df1[['tpep_pickup_datetime']].copy()
del df1


# In[5]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)


# In[6]:


df['WeekDay'] = df.tpep_pickup_datetime
df['YearWeek'] = df.tpep_pickup_datetime


# In[8]:


pandarallel.initialize(progress_bar=False)

df.WeekDay = df.WeekDay.parallel_apply(week_day)
df.YearWeek = df.YearWeek.parallel_apply(weekOfyear)


# In[9]:


z = pd.DataFrame((df.groupby(['WeekDay','YearWeek']).size()))
statistics = pd.DataFrame(z.values, columns=['viajes_amount'])


# In[10]:


# get index from statistics
day = list(range(0,z.values.shape[0]))
for idx, i in enumerate(z.index):
    day[idx] = i[0]

statistics['DayWeek'] = day


# In[11]:


f=statistics.DayWeek.unique()
days = f[[3, 1, 5, 6, 4, 0, 2]]
y0 = statistics.groupby('DayWeek').median().viajes_amount
y0 = y0[[3, 1, 5, 6, 4, 0, 2]]


# In[12]:


fig = go.Figure([go.Bar(x=days, y = y0)])
fig.show()

