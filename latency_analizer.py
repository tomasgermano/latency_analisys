import glob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
!pip install openpyxl

# define the path where the data sources are
path="/content/drive/MyDrive/Colab Notebooks/LATENCIA/"

# os.listdir() create a list with all the files in the path
directory_files = os.listdir(path)
directory_files

##Just for Google Colab because the platform has a hide file named ".ipynb_checkpoints"
#file_del = path + '.ipynb_checkpoints'
#if os.path.exists(file_del):
#    shutil.rmtree(file_del)

pd.DataFrame({}).to_csv("/content/drive/MyDrive/Colab Notebooks/LATENCIA_test.csv")
flujototal = pd.DataFrame()

#We read all files, split the filename with "_" as a separator and toke the first part as sourceIP to insert it as a new column
#Then, we append all data to a csv file
for index,file in enumerate(directory_files):
    origen = directory_files[index].split('_', 1)[0]
    df_file = pd.read_csv(os.path.join(path, file),sep=',',names=['all','origen'])
    df_file['origen'] = origen
    df_file.to_csv("/content/drive/MyDrive/Colab Notebooks/LATENCIA_test.csv",mode='a')

#Read the file csv, defining 3 columns
flujototal_f = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/LATENCIA_test.csv",names=['ID','all','origen'])
#Drop all the NA
flujototal_f = flujototal_f.dropna()
#As I mention in the "Data source structure and details" section, we have to drop lines with a strings that contain "*data bytes*"
#clean is a new dataframe with all the lines that meet the condition, then, we drop the lines in the original dataframe using "clean" as a filter
clean=flujototal_f[flujototal_f['all'].str.contains('data bytes*',na=False,case=False, regex=True)]
flujototal_f.drop(clean.index[:],inplace=True)#borro todas las líneas que estan en clean del dataframe original
flujototal_f.head()

#DATA PREPARATION
# If you execute a head to inspect the structure, you can notice that the icmp information hasn't a csv structure, insted of that, we have to deal with the string
# using diferent logics to parse it
# firstly we use the space to obtain diferent columns
flujototal_f[["dia", "hora", "size", "unidad", "4", "dst","icmp_seq","ttl","lat","unit_lat"]] = flujototal_f["all"].str.split(" ",expand=True)
# we creat a "timestamp" column concatenating day and hour
flujototal_f['timestamp'] = flujototal_f['dia'].astype(str) + ' ' + flujototal_f['hora'].astype(str)
flujototal_f['timestamp'] = pd.to_datetime(flujototal_f['timestamp'])
# we have to replace ":" to obtain the destination IP
flujototal_f["dst"] = flujototal_f["dst"].str.replace(':','')
# we replace "time=" in the "lat" column to obtain the latency
flujototal_f["lat"] = flujototal_f["lat"].str.replace('time=','')
flujototal_f['lat']= flujototal_f['lat'].astype(float)

# With this lines you can analize the latency looking for some patterns
#flujototal_f[flujototal_f['lat'] > 100]
#flujototal_f[flujototal_f['lat'] < 0]

#To obtain our first results, we can calculate the mean and maximus groupoing by source and destiny
flujototalxDST = flujototal_f.groupby(['origen','dst'])
flujototalxDST['lat'].agg(['mean', 'max'])
#flujototalxDST['lat'].describe() #obtain more statistics

#Because we want to analize the information by day and time, let build a new dataframe grouped by source, destiny, day and time.
flujototalxhoras = flujototal_f.groupby(['origen','dst',flujototal_f['timestamp'].rename("día").dt.day,flujototal_f['timestamp'].rename("hora").dt.hour])
# We can write the results in a excel file or show it on screen
#flujototalxhoras['lat'].describe().to_excel("estadisticas_latencia_2.xlsx")
flujototalxhoras['lat'].agg(['mean', 'max'])


#As a finale step, its totaly usefull to understand the results, make some graphs representing the latency in the time by source and destiny
for key, gp in flujototalxDST:
  gp.plot(x='hora',y='lat', figsize=(35, 8))
  plt.title(key)
