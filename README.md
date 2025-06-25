# 2024 Data Science Internship Project 
Given Navy HVAC data for aircraft carriers, our objective was to provide suggestions and reccomendations for improving the efficiency and effectiveness of these HVAC systems.
# Our Data
The data was given in two datasets. <br> <br>
The 'Jobs' dataset esentially provides information regarding why a maintenance action was necessary, where the problem was located, its level of perceived importance, and the timeline for completion. <br><br>
The 'Supply' dataset describes part orders for jobs in the 'Jobs' dataset. There could be anywhere from zero to several part orders associated with a maintenance record. 

# Data Cleaning and Exploration
Before modeling, we conducted data cleaning and exploratory data analysis. We:
- Removed columns with excessive missing values and standardized the data types across both the 'Jobs' and 'Supply' datasets
- Replaced missing values in categorical columns (either using the mode or creating an “unknown” category) and in numerical columns (using the median)
- Nomalized skewed numerical features using log transformations and Box-Cox transformations
- Identified and mitigated outliers using IQR
- Feature engineered new date-based features (year, month, day of week), and created variables such as maintenance_duration whhich ended up being our models' target variable


# Modeling
We built a Random Forest Regression model to predict the number of days that elapsed between the opening and closing of a maintenance action (maintenance_duration), and also for maintenance actions subsetted to PMS-related work. 
<br><br>
Our feature set includes features covering information such as the reason for repair, when a maintenance job was discovered, where on ship the equipment was located, and the severity of the issue prior to maintenance. 
<br><br>
After fitting the model with exclusively the categorical and quantitative variables within the dataset, we began considering ways to leverage the information contained in the free-form text columns. 
Some techniques we applied include Named Entity Recognition (NER), regular expression matching, and the Word2Vec algorithm. 
<br><br>
Our final models used numeric, categorical, and text-derived features.
<br>

# Interactive Dashboard

We also developed an interactive dashboard using Dash and Plotly, which visualizes maintenance activity on a 3D model of an aircraft carrier.

- Displays maintenance jobs by ship compartment in 3D, top, front, and side views
- Filters by:
  - Ship
  - Job maintenance feature (cause, action taken, etc.)
  - Date range
  - cost, days open, man-hours
- Clickable compartments display job details
- Aggregate statistics by ship (Total Material Cost, Days Open)

# Our Takeaways 
Our models predicting maintenance duration and the accompanying interactive dashboard can help improve resource and personnel allocation, logistic planning, and reduce unnecessary down time for components of the ship. 
