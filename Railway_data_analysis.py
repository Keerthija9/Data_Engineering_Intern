#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


df = pd.read_csv('Railway_info.csv')
df.head()


# In[4]:


df.describe()


# In[7]:


df.info()


# In[10]:


import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# In[11]:


sns.heatmap(df.isnull(),cbar= False, cmap='viridis', yticklabels=False)
plt.title('Heatmap:No Null values')
plt.xlabel('Columns')
plt.ylabel('Records')
plt.show()


# In[12]:


#Checking if there are any empty spaces

for col in ['Train_Name','Source_Station_Name','Destination_Station_Name','days']:
    empty_spaces = df[df[col].str.strip()=='']==1
print(empty_spaces.count())


# In[13]:


df.nunique() #gives all the unique values count in each coulmn


# In[14]:


# Finding most common stations

for col in ['Source_Station_Name','Destination_Station_Name']:
    print(df[col].value_counts().head())


# In[15]:


df.days.unique()


# In[16]:


#replacing days with correct day_name

df['days'] = df['days'].replace(r'd$','',regex=True) 
df['days'].unique()


# In[17]:


df.nunique()


# In[18]:


#Standardizing all station names into uppercase

for col in ['Source_Station_Name','Destination_Station_Name']:
    df[col].str.upper()
    print(df[col])


# In[20]:


All_stations = pd.concat([df['Source_Station_Name'],df['Destination_Station_Name']])
unique_stations = All_stations.drop_duplicates()
print(unique_stations.sort_values())


# In[30]:


#Extracting train details for Monday and tuesday

df.loc[df['days'].str.contains('Monday|Tuesday')]


# In[32]:


#Extracting train details with source station "Wardha Junction"

df.loc[df['Source_Station_Name']=='WARDHA JN.']


# In[34]:


trains_count = df['Train_Name'].drop_duplicates().count()
trains_count


# In[36]:


trains = df['Train_Name'].unique()
trains


# In[38]:


# Extracting number of trains from each station
station_trains = df.groupby(['Source_Station_Name'])['Train_No'].count().reset_index()
station_trains = station_trains.rename(columns={'Train_No':'No_of_trains'})
station_trains


# In[40]:


#Calculating average number of trains per day per station
# Count the number of trains per station per day
trains_per_day = df.groupby(['Source_Station_Name', 'days'])['Train_No'].count().reset_index()

# Find the most frequent daily train count per station
avg_trains_per_day = trains_per_day.groupby(['Source_Station_Name','days'])['Train_No'].max().reset_index()

# Rename column
avg_trains_per_day = avg_trains_per_day.rename(columns={'Train_No':'Avg_Train_count'})
avg_trains_per_day


# In[42]:


# Count the number of trains per day
train_counts = df['days'].value_counts().sort_index()

# Plot
plt.figure(figsize=(8,5))
sns.barplot(x=train_counts.index, y=train_counts.values, palette="viridis")
plt.xlabel("Days of the Week")
plt.ylabel("Number of Trains")
plt.title("Train Operations by Day of the Week")
plt.show()


# In[44]:


df['Route'] = df['Source_Station_Name'] + " → " + df['Destination_Station_Name']
top_routes = df['Route'].value_counts().head(15)

plt.figure(figsize=(12,6))
sns.barplot(y=top_routes.index, x=top_routes.values, palette="magma")
plt.xlabel("Number of Trains")
plt.ylabel("Train Routes")
plt.title("Most Frequent Train Routes")
plt.show()


# In[45]:


# Map weekdays to numerical values
days_mapping = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
df["days_numeric"] = df["days"].map(days_mapping)

# Count the number of trains per day
train_count_per_day = df.groupby("days_numeric")["Train_No"].count().reset_index()
train_count_per_day.columns = ["days_numeric", "train_count"]

# Compute correlation
correlation_matrix = train_count_per_day.corr()

# Display correlation heatmap
plt.figure(figsize=(6,4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Between Train Frequency and Days of Operation")
plt.show()

# Print correlation values
print(correlation_matrix)


# In[ ]:




