# solar

## solar irradiance prediction project


### Overview
The goal of this project is to practice collecting real world data, cleaning and preparing it, and using it to train models for prediction. 

### Data
See the [data folder](https://github.com/ian-double-u/solar/tree/master/data) to view the data I used and see [instructions.md](https://github.com/ian-double-u/solar/blob/master/data/instructions.md) to learn how to put it together yourself; including collecting your own solar irradiance data with [Vernier Sensors]([https://www.vernier.com/](https://www.vernier.com/)).


The data used in this project comes from two sources. NOAA's SURFRAD project and data collected personally. However, if you do not have access to the required hardware you can use SURFRAD data exclusively. 


The SURFRAD data is collected at 6 separate sites across the United States with very high fidelity (1 observation/minute). The geographic variety and vast quantity of data (going back many years) makes it perfect for training models.

In this project I use the SURFRAD data to train my model(s) and then use the irradiance data I collected myself as a test set.


### Modeling


If you are interested in experimenting with your own models you can use the template I have created to pre-process all of the data and insert your own model. This template can also be found [here](https://github.com/ian-double-u/solar/blob/master/model_template.py)


Otherwise, I provide an example of a model you could build to try and predict the irradiance data you observed. See the [model folder](https://github.com/ian-double-u/solar/tree/master/model) to view the model I experimented with.


### Conclusions
At the outset of the project I thought measuring would give me a interesting and a unique data set I could then use to build knowledge and experience of machine learning models. However, as seen in [instructions.md](https://github.com/ian-double-u/solar/blob/master/data/instructions.md) the collection, cleaning and preparation process is very involved and ended up being the area that I learned the most. 


The predictive models I built, though relatively competent on the SURFRAD data, had trouble predicting the data I collected myself. This again highlights the importance of the collection, cleaning and preparation phase of data science.


All in all this was a great project in many ways, regardless of the predictive capabilities of the result. Additionally, there are many ways this project could be tweaked to meet individual interests and goals. 
**I hope you find this project helpful and give it, or something inspired by it, a shot!**
