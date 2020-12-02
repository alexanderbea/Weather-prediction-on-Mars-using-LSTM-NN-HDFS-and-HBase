#run locally
import pandas as pd
import urllib.request, json
from subprocess import run

def write(df: pd.DataFrame, filename: str) -> object:
    df.to_csv('~/'+filename)
    run('$HADOOP_HOME/bin/hdfs dfs -put {} /mars-weather'.format(filename), shell=True)

loadHistoricalDataFrom = "API" #Drive or API works; Now we need to make HBase or work

#@title Functions: Load Data
def loadHistoricalData():
  if loadHistoricalDataFrom == "API":
    archiveUrl = 'https://pudding.cool/2017/12/mars-data/marsWeather.json'
    data = pd.DataFrame(pd.DataFrame(json.loads(urllib.request.urlopen(archiveUrl).read().decode('utf-8'))))
    return data
  elif loadHistoricalDataFrom == "Drive":
    data = pd.read_csv('/content/../mars-weather.csv')
    return data

dfArchive = loadHistoricalData()

# initiating publisher object and loading to hdfs calling the write method
write(dfArchive, 'archive.csv')