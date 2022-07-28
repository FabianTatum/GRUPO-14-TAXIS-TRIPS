#!/usr/bin/env python
# coding: utf-8

# In[2]:


import db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandarallel import pandarallel
import plotly.graph_objects as go


# In[3]:


def week_day(param):
    import datetime
    return param.strftime("%A")

def weekOfyear(param):
    import datetime
    return param.strftime("%W")


# In[4]:


df1 = db.conn(
    ''' 
    SELECT tpep_pickup_datetime
    FROM taxi_trips;
    '''
)


# In[5]:


df = df1[['tpep_pickup_datetime']].copy()
del df1


# In[6]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)


# In[7]:


df['WeekDay'] = df.tpep_pickup_datetime
df['YearWeek'] = df.tpep_pickup_datetime


# In[9]:


pandarallel.initialize(progress_bar=False)

df.WeekDay = df.WeekDay.parallel_apply(week_day)
df.YearWeek = df.YearWeek.parallel_apply(weekOfyear)


# In[10]:


z = pd.DataFrame((df.groupby(['WeekDay','YearWeek']).size()))
statistics = pd.DataFrame(z.values, columns=['viajes_amount'])


# In[11]:


# get index from statistics
day = list(range(0,z.values.shape[0]))
for idx, i in enumerate(z.index):
    day[idx] = i[0]

statistics['DayWeek'] = day


# In[12]:


f = statistics.DayWeek.unique()

boxes = list(range(0,7))
h = f[[3, 1, 5, 6, 4, 0, 2]]

for i in boxes:
    boxes[i] = np.array(statistics.viajes_amount[statistics.DayWeek == h[i]])


# In[13]:


fig = go.Figure()
for idx, i in enumerate(boxes):
    fig.add_trace(go.Box(y=i, name=h[idx],
                marker_color = 'blue'))

fig.show()

