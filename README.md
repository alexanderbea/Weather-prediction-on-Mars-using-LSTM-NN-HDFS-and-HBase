# Introduction
While life fl
ished and evolved on Earth, Mars has experienced significant climate change. Geologists that study planets can study rocks, sediment as well as solid to uncover the history of the surface. Scientists however, are interested in the water on Mars and want to understand how life can survive there. Craters, volcanoes, photochemical effects, geophysical processes and signs of weather conditions are all important aspects that unfold the history and future of Mars [1]. NASA has been tracking weather measurements such as temperature, wind speed, pressure atmospheric opacity since 2012. The problem here is that the weather conditions fluctuate during day and night as well as during seasons. There is a seasonality pattern which makes it a good candidate for prediction modelling. For the importance of understanding the future state of Mars and the changes that it will experience, this project provides the data-capture infrastructure and a prediction model to help with forecasting the weather on Mars with a deep learning model. <b>What has been done:</b> Firstly, file “HistTemp-file” is accessed and one api “CurrWeekTemp-API” which provides the historical daily temperature from Mars for a specific time period and another CurrWeekTemp-API that provides the most recent seven days. Secondly, the data from the HistTemp-file is imported to HDFS and HBase, whereafter extract this data in a Jupyter Notebook (python) “training-notebook” wherein a univariate single timp step recurrent neural network is built that trains on this data to predict one day ahead. This training model is then saved to disk, whereafter loaded the model from disk into another Jupyter Notebook (python) “predict-notebook” as well as the most recent seven days of temperature from CurrWeekTemp-API and predict the next day temperature.

# Datasets
One historical bulk file is utilized for this project and one api for the most recent seven days. “HistTemp-file” is a JSON file from “The Pudding”-repository, whereby the historical time series is fetched [2]. The data that has been made available by NASA’s Mars Science Laboratory as well as the Centro de Astrobiología (CSIC-INTA) and time interval (daily time series) includes data from Sol 1 (2012-08-07 on Earth) to Sol 1895 (2018-02-27 on Earth). The api “CurrWeekTemp-API” (‘InSight: Mars Weather Service API’ a.k.a “InSight API”) provides the most recent 7 days of temperature measurements [3]. 

# Solution & Result
The following presents the data flow of the historical data from HistTemp-file.  Firstly the data is loaded into HDFS and HBase using Python. The script “writeHdfs.py” accesses the file from The Pudding-repository and runs the terminal command to put the file into the HDFS as a comma separated value file. The file that is now stored in HDFS is then put into an HBase table by the HBase ImportTsv utility that will load data originally in TSV format into HBase. It is loading data from TSV format in HDFS into HBase via Puts. Next, one can pass an argument Dimporttsv.separator = ‘,’ to specify the comma as the deliminator. Next, the most recent 7 days of temperature data is loaded from the CurrWeekTemp-API into the saved prediction model. 

![](https://github.com/alexanderbea/Weather-prediction-on-Mars-using-LSTM-NN-HDFS-and-HBase/blob/main/Images/Figure%201.PNG)


As illustrated in Figure 1 the data is loaded into the training-notebook. Inside the training-notebook, the temperature data is normalized and batched up into 7 day’s batches, split the batches into training (70%), validation (15%) and test (15%), whereafter load it into the Recurrent Neural Network with Keras [4] through Tensorflow [5] and train, validate and test the model.  Next, the SGD optimizer is applied with MSE as a loss-function. Thereafter, apply one Long Short Term Memory (LSTM) layer with 128 neurons, one Bidirectional LSTM with 64 neurons and one Dense layer. The RNN model proved to be well-suited for the time series prediction task. It is mostly used to predict a future outcome based on the previous sequential inputs, it uses their memory (also called states) to predict sequence outputs [5]. The following  loss and mean absolute error (MAE) shows that the model successfully manages to optimize the learning of the training data and generalize it so that the validation shows successfully low loss and MAE rates:

![](https://github.com/alexanderbea/Weather-prediction-on-Mars-using-LSTM-NN-HDFS-and-HBase/blob/main/Images/Figure%202%20%26%203.PNG)

Next, apply the temperature prediction to test-data and plot it with the historical actual temperature data:

![](https://github.com/alexanderbea/Weather-prediction-on-Mars-using-LSTM-NN-HDFS-and-HBase/blob/main/Images/Figure%204.PNG)

In Figure 4, it becomes clear that the prediction is fairly accurate. Thereafter, save the model to disk so that one can load it in the prediction notebook in the next step. In the next Figure 5, plot the previous 7 days min, max and average temperature that have been loaded from the CurrWeekTemp-API in the prediction-notebook as well as the day-a-head average temperature prediction (marked red as a red star).

![](https://github.com/alexanderbea/Weather-prediction-on-Mars-using-LSTM-NN-HDFS-and-HBase/blob/main/Images/Figure%205.PNG)

# How to run the code
1. Create HDFS directory and fill with archive data:
- $HADOOP_HOME/bin/hdfs dfs -mkdir /mars-weather -- creates the directory for the archive data
- python3 writeHdfs.py -- runs the script that pulls the archive data into the ‘mars-weather’ directory

2. Pull data from HDFS into HBase
- cd /user/hbase -- then open the hbase shell and create target table>
- create ‘archive’, {NAME=> ‘cf’} -- exit hbase shell and execute following command
- hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=, -Dimporttsv.columns=’HBASE_ROW_KEY, cf:id, cf:date, cf:sol, cf:ls, cf:season, cf:min_temp, cf:max_temp, cf:pressure, cf:wind_speed, cf:atmo_opacity’ archive /mars-weather/archive.csv

3. Run the “ProjectNotebook_Training.ipynb” in Jupyter Notebook, 

- However first make sure that you set the parameter runLocallyOrOnDrive  to  'Drive' or 'Local' (if you are running it in Colab, ‘Drive’ is possible, however, you will have to link your Google Drive), this variable only saves the prediction model to drive or local disk
- Next, change the path to where you want to save the prediction model (the variable “saveModelPath” and “saveModelPathH5” need to be changed for this).
- Thereafter, select whether you want to extract the historical data from the Pudding-API or from HBase, API or Drive (define the variable loadHistoricalDataFrom to “HBASE”, "API" or “Drive)
- Now you can run the entire notebook

4. Now that you have run the training and saved the model to local or drive you can run the prediction-notebook “ProjectNotebook_NextDayPrediction.ipynb”
- Change the variable runLocallyOrOnDrive previously to what you choose to run before i.e. Drive or Local, now you can run the notebook

# References 
[1] ESA. 2020. The European Space Agency. Available from: <http://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Exploration/Why_go_to_Mars> [2020-10-21].

[2] Pudding. 2020. Digital publication that explains ideas debated in culture with visual essays. Available from: <https://pudding.cool/2017/12/mars-data/marsWeather.json> [2020-10-21].

[3] NASA. 2020. Insight Weather. Available from: <https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0> [2020-10-21].

[4] Keras. 2020. Recurrent layers. Available from: <https://keras.io/api/layers/recurrent_layers/lstm/> [2020-10-21].

[5] Tensorflow. 2020. Time series. Available from: <https://www.tensorflow.org/tutorials/structured_data/time_series> [2020-10-21].





