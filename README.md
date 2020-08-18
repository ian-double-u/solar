# solar

## solar irradiance prediction project


### Overview
The goal of this project is to practice collecting real world data, cleaning and preparing it, and using it to train models for prediction. Read on to walk-through the project.


### Data
See the [data folder](https://github.com/ian-double-u/solar/tree/master/data) to view the data I used and see [instructions.md](https://github.com/ian-double-u/solar/blob/master/data/instructions.md) to learn how to put it together yourself; including collecting your own solar irradiance data with [Vernier Sensors]([https://www.vernier.com/](https://www.vernier.com/)).


The data used in this project comes from two sources. NOAA's SURFRAD project and data collected personally. However, if you do not have access to the required hardware you can use SURFRAD data exclusively. 


The SURFRAD data is collected at 6 separate sites across the United States with very high fidelity (1 observation/minute). The geographic variety and vast quantity of data (going back many years) makes it perfect for training models.

In this project I use the SURFRAD data to train my model(s) and then use the irradiance data I collected myself as a test set.


Below are some examples of the data I collected with the pyranometer.
![Image One](https://lh3.googleusercontent.com/iVHSKQuMhFZ7Pjni4Yd0ju0DoB0A5Oi61dYcHsQHuNpykPziYbae_Qv8VtBWRJwAMu19jkxx3Y0qnU-6q92EPYn-SpR_LAHqQdJRhzc5_9O1aJ19FUenMpzqBPGn0z9HCPMoT_xrJezua4qsqXoZYuDTAveOMUG9W28FbnaOFz39KrqQDf63L1eVDrrS4pzFIsrW_Ap1xOIntnJ9Au-kcl9SH3ZVgEz8KZq4krMNCzIJ3GVz3jwYglNlQ2JnCSiK9UK60w7fvRlzYnk9uK9IwW3nzFcVD5shjQzPoZ_4GbiPBCOMTxEuPd8ueCmRa4_C6yWaMsuXETqybXFGOFxTf09DNZe1rM-O8InTxHeyRNIA8azVQ5QjMyCswzlGOHU5NfTUqibWgOSl3Jv2b8bA_fCHPi8HQ2qwEEotyQuZXf6UChTKYKcRUTcV46Ye7x-BHjXYUeClj9wufX3XX0eVZ3ppKZAphCWaeKAhKBWDVTPOUdDHR5df0SQMYI5Th3h7Ccy1obKf4V2T6x5dt86IGtZj_-flCCei4H92WbPVr7IJw_BXniSbVsrR-onA4sXzhcUUCBvoiEa-jd5lthedW2dLzp5qCNDvTkmZ6r_oq3PVENGpEIdizS-1_5nPewZIqlyNWaGEn3oazOjOEk22PCdxEAzKyVaU6wDfHZVrSNi9JLOerVjcY6Yw-pha=w424-h280-no?authuser=0) ![Image Two](https://lh3.googleusercontent.com/WK4RYmyNLFxp0AoOtRf-RkP6CaaRcxCC2y7wTrz-xTOEBD5L-SfWEYe0lb1h5LNs2DdhAaxhSbrC8dj8CuscaUA8FH8_oOj2qg3Qc3mE0zhqtM6sBhJfhdA8p2dd87_2_WPss-lKilMi3f6GWrTaUdnOIREzNczPi-M38zJ-jEE67JuEL_Z8qABfbUcfaB1DnzUZkt6TYjDTnbs9QIuxNxn1HP-a9G6NGGtlhyxPOsauln_d9ye50IO9X4oi6-aW0T864zMh57ifhqhW9XrFHNL8h1QEYbWE0zdrwYiIOAAplFuHnTiTfVQL46I-XQrk8cV4L024YSB57GzP5A2RLjIL_kafc3QymgkulCrUa_RmyG0q1ZI8UNuF55hVMGN5at_bd0NdZMONjkPAN-HSMYb2JQFDhn9m5vKbrp4Gc1LSGkVZccZxKGyLbZVP8kZlfhbse9hQdIuZPiqD4jCUjwIDXcLqi-Ma63KkP-6yrBGXgWeD0oxrcQF7TuUVMLtz037YoUIfoonVApk7GDV6xVRbghXbPrxfkfZ4DH3K6XtZlA6q9hA1iwS6aW5xmTZMSiZQ7HJLeIE5WXLFzAcC5VkzLE5O048R1fX8w_KftEnJ75HW_bv-4NHs3xkBY6kWAXM_kVcXEMm-WUmrDiK7cMTyBw315gyUffAfpSLIAmi0j0oHeVbQEXOC_uYd=w424-h280-no?authuser=0)
![Image Three](https://lh3.googleusercontent.com/iVHSKQuMhFZ7Pjni4Yd0ju0DoB0A5Oi61dYcHsQHuNpykPziYbae_Qv8VtBWRJwAMu19jkxx3Y0qnU-6q92EPYn-SpR_LAHqQdJRhzc5_9O1aJ19FUenMpzqBPGn0z9HCPMoT_xrJezua4qsqXoZYuDTAveOMUG9W28FbnaOFz39KrqQDf63L1eVDrrS4pzFIsrW_Ap1xOIntnJ9Au-kcl9SH3ZVgEz8KZq4krMNCzIJ3GVz3jwYglNlQ2JnCSiK9UK60w7fvRlzYnk9uK9IwW3nzFcVD5shjQzPoZ_4GbiPBCOMTxEuPd8ueCmRa4_C6yWaMsuXETqybXFGOFxTf09DNZe1rM-O8InTxHeyRNIA8azVQ5QjMyCswzlGOHU5NfTUqibWgOSl3Jv2b8bA_fCHPi8HQ2qwEEotyQuZXf6UChTKYKcRUTcV46Ye7x-BHjXYUeClj9wufX3XX0eVZ3ppKZAphCWaeKAhKBWDVTPOUdDHR5df0SQMYI5Th3h7Ccy1obKf4V2T6x5dt86IGtZj_-flCCei4H92WbPVr7IJw_BXniSbVsrR-onA4sXzhcUUCBvoiEa-jd5lthedW2dLzp5qCNDvTkmZ6r_oq3PVENGpEIdizS-1_5nPewZIqlyNWaGEn3oazOjOEk22PCdxEAzKyVaU6wDfHZVrSNi9JLOerVjcY6Yw-pha=w424-h280-no?authuser=0)
![Image Four](https://lh3.googleusercontent.com/32rA37Btrk_V4AkaCEgrTDOMA0qvRl5JdTWQlLdtTOL7M-CWLpiXxv9ZCGvwd0fFdNKVhJdVgQeyff7NmPnZ4cZZF9FfY47vKbCDCQuTwOZlfreQSWt3dms6PdFkbpil5nWSRc8hHGItIw3qJZ3P1US6JNg5cWb2HF_2Ro8NIaCmF9WVe8-aTiulmoxecHJ3pILpP4sEnTo3n_njeGmY0p196rGe0HKy2jngvPYzAZ2-c9eEPj0PksnzW3VRbS2qPMdi9La9gPZ0Ea3P3S2BRjufwo5sZ2_52h5UUBkmBcGmJfHfW5hTAt5-ubicEXG2Dg-zBAFfTodIxKQAXbfebU-gwacSgf9BU51h088psNzSnBoklLufXvqoyxcb3oXuv_iValAXOc_kRBEGGTj_5-V0Xhp6fc3r8oKAOx2c6KfNsOy9El-vO2XDOIrjMocaltflGbeK2_pA-54u7EYFOGVFEPexZTZZyI_gUPWb39uUD1SyLHGG3ZMowvc10K9FKQ7w22jMQC1tRuMcnJpFFX-m1PEEPg7sfSuzbtwTCaYUT4S18GwSUpF7uB3v2_mki38N2QZ1PsSY3c1GLSSblH5Xf6ERYnZYU5qZS1GFT1KFUeIAYiZ1kT9D9fNQtTKYaCmZ-sbnn5QWg1l4c76CW1u1vu56IPoDTVfU8Ohl_5OFobtiLOyNtq4Ag1M4=w424-h280-no?authuser=0)

### Modeling


If you are interested in experimenting with your own models you can use the template I have created to pre-process all of the data and insert your own model. This template can also be found [here](https://github.com/ian-double-u/solar/blob/master/model_template.py)


Otherwise, I provide an example of a model you could build to try and predict the irradiance data you observed. See the [model folder](https://github.com/ian-double-u/solar/tree/master/model) to view the model I experimented with.


### Conclusions
At the outset of the project I thought measuring would give me a interesting and a unique data set I could then use to build knowledge and experience of machine learning models. However, as seen in [instructions.md](https://github.com/ian-double-u/solar/blob/master/data/instructions.md) the collection, cleaning and preparation process is very involved and ended up being the area that I learned the most. 


The predictive models I built, though relatively competent on the SURFRAD data, had trouble predicting the data I collected myself. This again highlights the importance of the collection, cleaning and preparation phase of data science.


All in all this was a great project in many ways, regardless of the predictive capabilities of the result. Additionally, there are many ways this project could be tweaked to meet individual interests and goals. 
**I hope you find this project helpful and give it, or something inspired by it, a shot!**
