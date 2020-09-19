# -*- coding: utf-8 -*-
"""MexicoData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hqi63fZVwhGI1iNAEi8GMywCf2amMLNf
"""

import pandas as pd
df = pd.read_csv("/content/200918COVID19MEXICO.csv", encoding = "ISO-8859-1")
df.head(10)

df = df.rename(columns = {'FECHA_ACTUALIZACION': 'date',
                                  'ID_REGISTRO':'id',
                                  'ORIGEN': 'origin',
                                  'SECTOR': 'sector',
                                  'ENTIDAD_UM': 'care_unit_location',
                                  'SEXO': 'sex',
                                  'ENTIDAD_NAC': 'birth_state',
                                  'ENTIDAD_RES': 'residence',
                                  'MUNICIPIO_RES': 'city',
                                  'TIPO_PACIENTE': 'patient_type',
                                  'FECHA_INGRESO': 'entry_date',
                                  'FECHA_SINTOMAS': 'date_begin_symptoms',
                                  'FECHA_DEF': 'date_death',
                                  'INTUBADO': 'intubed',
                                  'NEUMONIA': 'pneumonia',
                                  'EDAD': 'age',
                                  'NACIONALIDAD': 'nationality',
                                  'EMBARAZO': 'pregnancy',
                                  'HABLA_LENGUA_INDIG': 'speaks_indig_language',
                                  'DIABETES': 'diabete',
                                  'EPOC': 'COPD',
                                  "RESULTADO":"result",
                                  "OTRO_CASO":"cov_contact",
                                  "TABAQUISMO":"tobacco",
                                  "RENAL_CRONICA":"chronic_kindney",
                                  "OBESIDAD":"obesity",
                                  "CARDIOVASCULAR":"cardiovascular",
                                  "OTRA_COM":"other_diseases",
                                  "HIPERTENSION":"hypertension",
                                  "INMUSUPR":"immunosuppression",
                                  "ASMA":"asthma",
                                  "MIGRANTE":"migrante",
                                  "PAIS_NACIONALIDAD":"nationality",
                                  "PAIS_ORIGEN":"departure",
                                  'UCI': 'ICU', })
df = df.drop(columns=['date','origin','sector','care_unit_location','birth_state','residence','city',
                              'patient_type','entry_date','date_begin_symptoms','nationality','speaks_indig_language',
                              'migrante','nationality','departure'])
df.columns
df.head(10)

filtered = df.loc[(df['intubed'] < 97) &
                  (df['pneumonia'] < 97) &
                  (df['pregnancy'] < 97) &
                  (df['diabete'] < 97) &
                  (df['COPD'] < 97) &
                  (df['asthma'] < 97) &
                  (df['immunosuppression'] < 97) &
                  (df['hypertension'] < 97) &
                  (df['other_diseases'] < 97) &
                  (df['cardiovascular'] < 97) &
                  (df['obesity'] < 97) &
                  (df['chronic_kindney'] < 97) &
                  (df['tobacco'] < 97) &
                  (df['cov_contact'] < 3) &
                  (df['result'] < 3) &
                  (df['ICU'] < 97)]
filtered.loc[df.date_death == '9999-99-99', 'death'] = 1
filtered.loc[df.date_death != '9999-99-99', 'death'] = 2
filtered = filtered.drop(columns=['date_death'])
filtered["death"] = filtered["death"].astype(int)
# filtered.dtypes

filtered.reset_index(drop=True, inplace=True)

filtered.loc[:, (filtered.columns != 'age') & (filtered.columns != 'id')] = filtered.loc[:, (filtered.columns != 'age') & (filtered.columns != 'id')].apply(lambda col: col - 1)
filtered.head(10)



from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X = filtered.loc[:, (filtered.columns != 'id') & (filtered.columns != 'result')]
y = filtered.loc[:, filtered.columns == 'result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

logisticRegr = LogisticRegression()
logisticRegr.fit(X_train, y_train)
predictions = logisticRegr.predict(X_test)
score = logisticRegr.score(X_test, y_test)
print('Accuracy of logistic regression classifier on test set: {:.4f}'.format(score))
from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))
import pickle

pickle.dump(logisticRegr, open("/content/preconditionLogReg.pkl", "wb"))

logisticRegr = pickle.load(open("/content/preconditionLogReg.pkl", "rb"))
score = logisticRegr.score(X_test, y_test)
print(score)

from sklearn import svm
import numpy as np
X = filtered.loc[:, (filtered.columns != 'id') & (filtered.columns != 'result')]
y = filtered.loc[:, filtered.columns == 'result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

svm_model = svm.SVC()
svm_model.fit(X_train, np.ravel(y_train))

predictions = svm_model.predict(X_test)
score = svm_model.score(X_test, y_test)
print('Accuracy of svm classifier on test set: {:.4f}'.format(score))
from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))

def precondition_risk(x):
  preconditionLogisticRegr = pickle.load(open("model/preconditionLogReg.pkl", "rb"))
  return preconditionLogisticRegr.predict_proba([x])[0][1]
precondition_risk(X_test.loc[0,:])
