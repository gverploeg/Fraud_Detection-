<div align="center">  
<header>
    <h1>Who You Gonna Call?<br>
    Fraud-Busters</h1>
  </header>
<div align='left'>  

<div align="center"> 
<img src="images/Fraud-Busters.png" class="center">
<div align='left'> 


## Table of Contents
1. [Background](#background)
2. [Data](#data)
3. [EDA](#eda)
4. [Models and Analysis](#models-and-analysis)
5. [Web App](#web-app)
6. [Future Work](#future-work)

## Background

Our team, the Fraud-Busters, was hired by an e-commerce site to weed out fraudsters. The fraudsters sent emails to users with fraudulent event tickets for purchase, and the e-commerce site would like to alert the consumers that the event tickets are fraudulent before they purchase them. The e-commerce site would like a web application that can be used to quickly triage potential fraudulent transactions as low risk, medium risk or high risk.   


## Data  

### Initial Data
We started with a json file of the current data from the e-commerce site. All of the date columns had to be converted to datetime from a Unix timestamp in seconds. We cleaned up the email and organization description features from HTML to standard text for easier interpretation in our models.  

We engineered a target column ```Label``` that is set to 1 if the transaction is fraudulent and 0 if it is not fraud based on the data in the ```acct_type``` column. 

![](images/num_fraud.svg)

## EDA


### Can We See a Difference in Words Used?

![](images/notfraud_words.svg)  

![](images/fraud_words.svg)  

### Cleaning Up the Feature Matrix

We decided to drop any features that were text heavy or included dates after more EDA as they did not seem to relate to the difference between fraud and not-fraud. We then engineered features by parsing out some of the original ones such as:
-  ```Ticket_Types``` was engineered into ticket cost, ticket availability, and amount of total tickets
    - Quantity Sold was not included as it may not be immediately processed when the data comes in
-  ```Previous_Payouts``` was engineered into a boolean (1 or 0) for if there was a previous payout or not

## Models and Analysis

### Choosing Our Model
Our team decided to build a variety of baseline models to compare before settling on the best model:
- KNN
- Logistic Regression
- SVM Support Vector Clustering (SVM-SVC)
- Random Forest

We compared models using the following three metrics:
> **Precision** - How many selected items are relevant  
> **Recall** - How many relevant items are correctly selected  
> **F1-score** - Better measure of the incorrectly classified cases than Accuracy

For our model, with Fraud = 1 (true positive), a high recall score would imply we are correctly identifying all fraudulant transactions and reducing false negatives; thus, if we are flagging user accounts to prevent theft we would not miss any. However, if we are discussing cost relating to investigating transactions, we would want a high precision score which implies we are reducing the number of false positives (falsely identified as a threat). The F-1 Score was the best metric to use as it blends precision and recall allowing us to choose the model that is performing the best at classifying a transaction as Fraud or Not-Fraud. For this reason, we chose to move forward with our random forest model. 

<div align="center">   

| **Model** | **Precision** |  **Recall** | **F-1 Score** |  
| :------: | :--------: | :-------: | :---------: |  
|K-Nearest Neighbors | 0.68 | 0.51 | 0.58 |  
| Logistic Regression | 0.92 | 0.78 |  0.84 |  
| SVM | 0.14| 0.82| 0.24 |  
|**Random Forest** | **0.95** | **0.91** |**0.93** |   

<div align='left'>  


### Final Model

After tuning our hyperparameters with a grid search, we finalized our Fraud-Busters random forest fraud detection model and saved it with [pickle](src/bestRTModel.pkl). 

We investigated which features of the data were most important in flagging an incoming transaction as fraud or not-fraud. Based on the feature importances from our model, ```Previous_Payout``` is the most important factor affecting if a transaction is flagged as fraud or not-fraud. 

![](images/rf_featureimportance.svg)
### Live Data
We created a pipeline for taking in live [data](http://galvanize-case-study-on-fraud.herokuapp.com/data_point) and configuring it to run through our pickled model. The incoming data is stored in a database along with the prediction that is returned from running the data through the model. 

### Predicting with Our Model

We created a prediction script that takes in the configured transaction data and outputs the predicted probability of the transaction being fraudulent. Each predicted probability is then stored in the database with its corresponding row of data.

### What is Fraud?  

Failures are not created equal:
-  False positives decrease customer trust
-  False negatives cost money, and not all of those cost the same amount of money

The model will not necessarily flag incoming transactions as fraud or not fraud, but instead allows the transactions to be flagged as needing further review due to the risk level. This is why the model is one that triages the most pressing (aka costly) transaction coming in.

### Triage Fraud Risk

We decided to triage the risk of fraud based on average ticket cost and average total ticket quantity as shown below. 

<div align="center">    

|     | **Low-Risk** | **Medium-Risk** | **High-Risk**|  
|:----:|:------:|:------:|:-----:|  
|**Average Ticket Cost** |  $0-$25| $25.01-$100 | >$100 |  
|**Average Ticket Quantity** | 0-10 tickets | 11-40 tickets | >40 tickets|  
|**Suggestions**| Don't Investigate | Flag for Future Investigation | Investigate Right Away|

<div align='left'>  

## Web App

### Fraud Scoring Service

![](images/risk_assessment.png)

## Future Work

We would love to receive feedback and improve our model with future work, such as:
- Additional hyperparameter tuning and increase the number of features through engineering
- Create more/improve triage values depending on the most important features, remove outliers, etc.
- Deploy this web application to a remote server (Heroku/AWS/GCP) instead of hosting locally
- Determine cost to the company for investigating fraudulent transactions using our model



