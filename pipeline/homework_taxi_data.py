#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[40]:


url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
df_taxi= pd.read_parquet(url)
df_taxi


# In[12]:


df_zone = pd.read_csv(f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')
df_zone


# In[29]:


get_ipython().system('uv add sqlalchemy psycopg2-binary')


# In[30]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[36]:


print(pd.io.sql.get_schema(df_taxi, name='green_taxi_data', con=engine))


# In[37]:


df_taxi.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')


# In[38]:


print(pd.io.sql.get_schema(df_zone, name='taxi_zone_data', con=engine))


# In[39]:


df_zone.head(0).to_sql(name = 'taxi_zone_data',con=engine, if_exists = 'replace')


# In[43]:


get_ipython().system('uv add tqdm')


# In[45]:


from tqdm import tqdm


# In[47]:


df_taxi.to_sql(name='green_taxi_data', con=engine, if_exists='append')


# In[48]:


len(df_taxi)


# In[49]:


df_zone.to_sql(name = 'taxi_zone_data', con=engine,if_exists='append')

