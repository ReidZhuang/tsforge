# tsforge
### Tsforge is a Python library for time series feature engineering. It is mainly designed for machine learning modeling before the feature engineering process. It can transform time series data into feature data with low cost, serving users who do not have the conditions to use deep learning algorithms to process machine learning data, or who want to use expert knowledge to develop customized features.

### tsforge requires the following packages:
- numpy
- scipy

## Purpose
tsforge is a tool to generate continuous time series data into features for future modeling demands. It is suitable for users who have time series data and want to build a forecasting model with it, and who want to extract features from the time series data without too much computation burden. tsforge is especially for those who prefer customized features extracted from time series data because they want to build forecasting models based on their valued professional experience, which deep learning methodology may not work as effectively and efficiently.

tsforge functions better on continuous data type. Most of the features are designed to represent continuous time series data’s features. Only a few are designed to represent classified time series data’s features.

tsforge is part of a larger ecosystem of Python libraries for data science and machine learning, such as pandas, numpy, scipy, and scikit-learn. It can be used as a preprocessing step before applying other machine learning algorithms or models to the feature data.

## Parameters
To use this tool, you need to specify two required parameters and five optional parameters (although we highly recommend you to enter all seven parameters to customize your own features). The parameters are:

- **cterm**: This is the number of time steps that defines a period from the most recent time step to a past time step that you think is important. This parameter cannot be larger than the total number of time steps of the input data.
- **checkday_list**: This is a list of time steps from the most recent time step to the past. The values of the time steps in this list will be extracted as features. The values from the past will be compared to the latest value to generate categorical variables. Any value in this list cannot be larger than the total number of time steps of the input data.
- **period_list**: This is a list of time steps from the most recent time step to the past. The time series data from the time step in this list to the most recent step will be considered as important. Statistics will be calculated from the periodical time series data. The default value is [10, 30, 60]. Any value in this list cannot be larger than the total number of time steps of the input data.
- **mode_round_number**: This is the rounding standard when calculating the mode for the time series. 1 means round up to the nearest integer. -1 means round up to the nearest 10-digit number. Choosing a suitable mode_round_number will give you better mode features. The default value is -1.
- **margin_value**: This is the upper threshold value of the time series data to reach. The default value is 500. This value should be smaller than the maximum of the input data.
- **special_cnt_value**: This is the value that you care about how many times it appears in a certain time period. The default value is 0.
- **period_comparison_base**: This is a list of time steps that the tool will use to compare two periods of time series data. For example, if the list is [10], the tool will take period A (10 time steps from the most recent step) and period B (10 time steps before period A) and compare their statistics. 

## Code Example
This is a demo of how to use tsforge to transform time series data into feature data that is ready for modeling. 

First, import tsforge and numpy. Then, create a numpy array with some random time series data. In this example, we have 30 time series, each with 200 time steps:
```python
import tsforge
import numpy as np
arr = np.random.rand(30, 200)*100
```
Next, specify the parameters for the feature engineering process. The parameters are:
```python
cterm = 70
checkday_list = [5, 10, 15, 20, 30, 40, 50, 60]
period_list = [10, 30, 60]
mode_round_number = -1
margin_value = 90
special_cnt_value = 0
period_comparison_base = [10, 30]
```
After setting up the parameters, create an instance of the tsforge class by using the forge_setup method:
```python
tsf = tsforge.forge_setup(cterm, checkday_list, period_list, mode_round_number, margin_value, special_cnt_value, period_comparison_base)
```
Then, use the check_para method to check if the parameters are valid:
```python
tsf.check_para(arr)
```
Finally, use the pull_features method to generate the feature data from the time series data. This method will return two variables: the first one is the feature data in numpy.array format, and the second one is a list of feature names:
```python
f_arr, f_index =  tsf.pull_features(arr)
```
You can now use the feature data for your modeling purposes.

## Features
This typical features the the model generated from the time series data:

- **recent60d_roll_net**: This is the net value of the time series from the last 60 time steps to the most recent time step. This feature reflects the overall trend of the time series in the last 60 time steps.
- **5terms_ago_difference**: This is the difference between the most recent value and the value 5 time steps ago. This feature reflects the change of the time series in a short term.
- **5terms_ago_diff_label**: This is a label that indicates whether the most recent value is equal to the value 5 time steps ago. This feature reflects the stability of the time series in a short term.
- **recent5terms_status_change_label**: This is a label that indicates whether the most recent value has changed during the last 5 time steps. This feature reflects the volatility of the time series in a short term.
- **10terms_ago_difference**: This is the difference between the most recent value and the value 10 time steps ago. This feature reflects the change of the time series in a medium term.
- **10terms_ago_diff_label**: This is a label that indicates whether the most recent value is equal to the value 10 time steps ago. This feature reflects the stability of the time series in a medium term.
- **recent10terms_status_change_label**: This is a label that indicates whether the most recent value has changed during the last 10 time steps. This feature reflects the volatility of the time series in a medium term.
- **15terms_ago_difference**: This is the difference between the most recent value and the value 15 time steps ago. This feature reflects the change of the time series in a long term.
- **15terms_ago_diff_label**: This is a label that indicates whether the most recent value is equal to the value 15 time steps ago. This feature reflects the stability of the time series in a long term.
- **recent15terms_status_change_label**: This is a label that indicates whether the most recent value has changed during the last 15 time steps. This feature reflects the volatility of the time series in a long term.
- **20terms_ago_difference**: This is the difference between the most recent value and the value 20 time steps ago. This feature reflects the change of the time series in a very long term.
- **20terms_ago_diff_label**: This is a label that indicates whether the most recent value is equal to the value 20 time steps ago. This feature reflects the stability of the time series in a very long term.
- **recent20terms_status_change_label**: This is a label that indicates whether the most recent value has changed during the last 20 time steps. This feature reflects the volatility of the time series in a very long term.
- **30terms_ago_difference**: This is the difference between the most recent value and the value 30 time steps ago. This feature reflects the change of the time series in a very very long term.

For more information, please check the demo file.
                      
## Contribution
Tsforge is an open source project, and we welcome contributions from anyone who is interested in improving it. If you want to contribute, please follow these steps:

Fork the repository and clone it to your local machine.
Create a new branch for your feature or bug fix.
Make your changes and commit them with clear and informative messages.
Push your branch to your forked repository and create a pull request to the master branch of the original repository.
Wait for the review and feedback from the maintainers.
Before you contribute, please read the code of conduct and the contributing guidelines for more details.

## License
tsforge is licensed under the Apache License, Version 2.0. See the license file for more information.

## Contact
If you have any questions, suggestions, or feedback, please feel free to contact me at Reid.Zhuang@icloud.com. You can also open an issue or a discussion on the GitHub repository. I appreciate your interest and support for tsforge. Thank you! 😊


