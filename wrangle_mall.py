import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import env

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def get_mall_customers(sql):
	    url = get_db_url('mall_customers')
	    mall_df = pd.read_sql(sql, url, index_col='customer_id')
	    return mall_df

def wrangle_mall_df():
    
    # acquire data
    sql = 'select * from customers'

    # acquire data from SQL server
    mall_df = get_mall_customers(sql)
    
    # handle outliers
    mall_df = outlier_function(mall_df, ['age', 'spending_score', 'annual_income'], 1.5)
    
    # get dummy for gender column
    dummy_df = pd.get_dummies(mall_df.gender, drop_first=True)
    mall_df = pd.concat([mall_df, dummy_df], axis=1).drop(columns = ['gender'])
    mall_df.rename(columns= {'Male': 'is_male'}, inplace = True)
    # return mall_df

    # split the data in train, validate and test
    train, test = train_test_split(mall_df, train_size = 0.8, random_state = 123)
    train, validate = train_test_split(train, train_size = 0.75, random_state = 123)
    
    return min_max_scaler, train, validate, test

def min_max_scaler(train, valid, test):
    '''
    Uses the train & test datasets created by the split_my_data function
    Returns 3 items: mm_scaler, train_scaled_mm, test_scaled_mm
    This is a linear transformation. Values will lie between 0 and 1
    '''
    num_vars = list(train.select_dtypes('number').columns)
    scaler = MinMaxScaler(copy=True, feature_range=(0,1))
    train[num_vars] = scaler.fit_transform(train[num_vars])
    validate[num_vars] = scaler.transform(validalidate[num_vars])
    test[num_vars] = scaler.transform(test[num_vars])
    return scaler, train, valid, test