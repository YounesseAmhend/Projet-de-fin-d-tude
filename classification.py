import pandas as pd
from table_logger import TableLogger
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# la liste de noms de variables qui seront utilisées dans l'analyse des données
variables = [
    "Gender", "Age", "Education", "Work", "Cardiac_Arrest_Admission", "Non_Cardiac_Condition",
    "Hypertension",  "Dyslipidemia","DM", "Year_DM_Diagnosed", "DM_Duration", "DM_Type",
    "DM_Treatment", "Smoking_History", "Waist", "BMI", "Fasting_Blood_Glucose_Value_SI_Units",
    "HbA1C_Admission_Value", "Lipid_24_Collected", "Cholesterol_Value_SI_Units",
    "Triglycerides_Value_SI_Units", "Creatinine_Clearance", "Heart_Rate"
]

df = pd.read_csv("csv/finalResult_MI.csv", usecols=variables)
# toutes les lignes contenant des valeurs manquantes sont supprimées :
df = df.dropna(axis=0)
# stocker tous les variables et sont valeur dans X sauf DM
X = df.drop("DM", axis=1)
# stocker les valeurs de DM dans y
y = df["DM"]

# diviser les données en ensembles d'apprentissage et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=42)

# normaliser les données d'apprentissage et de test
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# créer un modèle SVM (Support Vector Machine)
clf = SVC(kernel='rbf', C=1.0, gamma='auto')
# Entraînement du modèle

clf.fit(X_train, y_train)

# Entraînement du modèle
y_pred = clf.predict(X_test)

tb = TableLogger(columns='DMImputed,Accuracy,Precision,Recall,F1_score',
                 default_colwidth=12,
                 float_format='{:,.2f}'.format)
# Évaluation du modèle
tb(
   "No",
   "{:.2f}".format(accuracy_score(y_test, y_pred)*100) + " %", 
   "{:.2f}".format(recall_score(y_test, y_pred, pos_label=2)*100) + " %",
   "{:.2f}".format(recall_score(y_test, y_pred, pos_label=2)*100) + " %",
   "{:.2f}".format(f1_score(y_test, y_pred, pos_label=2)*100)+ " %"
)

# la meme chose mais tous les variables sont imputer
df = pd.read_csv("csv/FinalResultImputEverything_MI.csv", usecols=variables)

X = df.drop("DM", axis=1)
y = df["DM"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)



clf = SVC(kernel='rbf', C=1.0, gamma='auto')
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
tb(
   "Yes",
   "{:.2f}".format(accuracy_score(y_test, y_pred)*100) + " %", 
   "{:.2f}".format(recall_score(y_test, y_pred, pos_label=2)*100) + " %",
   "{:.2f}".format(recall_score(y_test, y_pred, pos_label=2)*100) + " %",
   "{:.2f}".format(f1_score(y_test, y_pred, pos_label=2)*100)+ " %"
)
tb.print_line(("+"+"-"*14)*5+"+")