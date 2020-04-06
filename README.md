# ASHRAE Great Energy Predictor III solution

This is my solution for [**ASHRAE - Great Energy Predictor III**](https://www.kaggle.com/c/ashrae-energy-prediction/overview) competition on Kaggle. I didn't succeed to take a high place, but [helped the community](https://www.kaggle.com/serengil/ucb-data-leakage-site-4-81-buildings/comments#689180) to find errors in leaks, used as validation data by many participants. The [Leak Data Station](https://www.kaggle.com/yamsam/ashrae-leak-data-station) author eventually became the competition winner :)

Data quality was the main problem in this competition, so data cleaning was my primary goal. This competition showed to me the difference between business and competition approach (excluding outliers from comparison _VS_ [multiplying forecasts by ~0.9](https://www.kaggle.com/c/ashrae-energy-prediction/discussion/123528)).

I implemented a pipeline for making forecasts in 4 Jupyter notebooks:
1. Data import.
2. Data cleaning
3. Datamart assembly.
4. Models training and inference.

The notebooks provide interactive widgets for data quality checks, using which I found errors.

You can download input data [here](https://www.kaggle.com/c/ashrae-energy-prediction/data) (it's around 400 MB so I didn't uploaded it to GitHub).
