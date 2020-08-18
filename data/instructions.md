# How I gathered my_data.csv and surfrad_data.zip

## my_data.csv 

**Required Hardware/Software**
+ [Vernier Pyranometer](https://www.vernier.com/product/pyranometer/)
+ [Vernier Go!Link](https://www.vernier.com/product/golink/)
+ [Vernier Graphical Analysis 4](https://www.vernier.com/product/graphical-analysis-4/)
+ Python 3 and Packages
+ [Geo_JSON object]([http://geojson.io/](http://geojson.io/)) of observation site
+ [Planet API Key]([https://www.planet.com/](https://www.planet.com/))

**<ins>Step 1.</ins>** Collecting raw irradiance data


Using the Vernier sensor collect solar irradiance data at desired location and when done collecting save data as a .csv file.
It is recommended that you take measurements at an interval of 1-5 minutes. This project uses an interval of 1 minute.
> Note: You must record the time of you start your experiment.


**<ins>Step 2.</ins>** Adding times, and related columns


Run [time.py](https://github.com/ian-double-u/solar/blob/master/time.py) to add the local time of each observation you collected. At this point you should have various .csv files for each of the observation sessions you have completed, where each file has the measured solar irradiance and the time of the observation. Do not proceed to the next step until you have completed all of the observations you would like to.

Next, run [my_data_prep.py](https://github.com/ian-double-u/solar/blob/master/my_data_prep.py) to add the other columns we need for our project. This scrip is run on all of the .csv files you have for the individual observation sessions. At the end of this step you should have a single .csv file with all of your data. You should get look something like [this](https://github.com/ian-double-u/solar/blob/master/data/my_data.csv), or just use that file if you do not collect data of your own.


## surfrad_data.zip

Step 1. Download data

You can get the SURFRAD dataset in one of two ways. The first would be to use the data set in this repo, found [here](https://github.com/ian-double-u/solar/blob/master/data/surfrad_data.zip), however that is only two months of data (whereas NOAA has years worth of minute by minute observations). 

The other (recommended) way would be to select and download the data you would liek with a script I have created for that purpose.  The NOAA data is stored [here](https://www.esrl.noaa.gov/gmd/grad/surfrad/).  Run [surfrad_download.py](https://github.com/ian-double-u/solar/blob/master/surfrad_download.py) to download data from all 6 NOAA stations for a given date range. 


Step 2. Prepare data


Next, in the same directory as you have the SURFRAD .dat files saved run [surfrad_data_prep.py](https://github.com/ian-double-u/solar/blob/master/surfrad_data_prep.py) to get surfrad_data.csv which is all of the SURFRAD data you will need. 


You have now collected and prepared all of the data needed for this project!
