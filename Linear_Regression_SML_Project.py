# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VYNy-Sg8g7WMDYITy3zqQpLecv0wQOpn
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/output_data.csv',)

import datetime
l1=[]
l2=[]
k=[]
i=0
for i in range(len(df)):
  l1.append(datetime.datetime.strptime(df['Q_CreationDate'].iloc[i],"%Y-%m-%dT%H:%M:%SZ"))
  l2.append(datetime.datetime.strptime(df['A_CreationDate'].iloc[i],"%Y-%m-%dT%H:%M:%SZ"))
  k.append((l2[i]-l1[i]).seconds//60)

df['Y']=k

h=[]
w=[]
i=0
for i in range(len(df)):
  if(l1[i].weekday()>=5):
    w.append(1)
  else:
    w.append(0)
  if(l1[i].hour>12):
    h.append(1)
  else:
    h.append(0)

df['weekend']=w
df['dayhalf']=h
df=df.drop(columns=['Q_CreationDate','A_CreationDate'])

df['Y'].head()

le = preprocessing.LabelEncoder()
le.fit(df['tags'])

df['tags']=le.transform(df['tags'])

scaler = preprocessing.MinMaxScaler().fit(df[['tags']])

df['tags']=scaler.transform(df[['tags']])

x=df.loc[:,df.columns!='Y']
y=df['Y']
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)

# from sklearn.feature_selection import RFE
# from sklearn.linear_model import LogisticRegression
# logreg = LogisticRegression()
# logreg.fit(x_train,y_train)

import statsmodels.api as sm
x_train_lm = sm.add_constant(x_train)
lr_1 = sm.OLS(y_train, x_train_lm).fit()

lr_1.summary()

cols=list(lr_1.pvalues[lr_1.pvalues<0.0005].index)
cols

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 1000
                                      )

# cols.remove('const')
x=x[cols]
y=df['Y']

mlr = LinearRegression()
mlr.fit(x_train,y_train)

y_pred_mlr= mlr.predict(x_test)
mlr_diff = pd.DataFrame({'Predicted Response time': y_pred_mlr})
mlr_diff.head()
