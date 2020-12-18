import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import pickle

from stephen_pipeline import prediction
request = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').json()

if __name__ == '__main__':
    print(prediction(request)[0][1])