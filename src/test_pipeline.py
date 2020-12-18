import requests
from stephen_pipeline import predict_fraud

getpred = predict_fraud(requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json())


if __name__ == '__main__':
    print(getpred.prediction(getpred.request[0][1])