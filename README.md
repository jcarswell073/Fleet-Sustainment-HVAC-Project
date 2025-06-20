# 2024 Data Science Internship Project 
Given Navy HVAC data for aircraft carriers, our objective was to provide suggestions and reccomendations for improving the efficiency and effectiveness of these HVAC systems.
# Our Data
The data was given in two datasets. <br> <br>
The 'Jobs' dataset esentially provides information regarding why a maintenance action was necessary, where the problem was located, its level of perceived importance, and the timeline for completion. <br><br>
The 'Supply' dataset describes part orders for jobs in the 'Jobs' dataset. There could be anywhere from zero to several part orders associated with a maintenance record. 

# Our Approach
We built a Random Forest model predicting the number of days that elapsed between the opening and closing of a maintenance action. 
<br><br>
We began by fitting a baseline linear regression model to make this prediciton. This model included approximately ten features covering information such as the reason for repair, when it was discovered, where the equipment was located, and the severity of the issue prior to maintenance. 
<br><br>
After fitting this baseline model with exclusively the categorical and quantitative variables within the dataset, we began considering ways to leverage the information contained in the free-form text columns. 
Some techniques we applied include Named Entity Recognition (NER), regular expression matching, and the Word2Vec algorithm. 
<br>

# Our Takeaways 
Our model predicting maintenance duration is intended to improve resource and personnel allocation, logistic planning, and reduce unnecessary down time for components of the ship. 
