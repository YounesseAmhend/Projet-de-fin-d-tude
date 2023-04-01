import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from table_logger import TableLogger
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# la liste de noms de variables qui seront utilisées dans l'analyse des données sauf "Year_DM_Diagnosed" et "DM_Duration".
variables = [
    "Gender", "Age", "Education", "Work", "Cardiac_Arrest_Admission", "Non_Cardiac_Condition",
    "Hypertension",  "Dyslipidemia","DM",  "DM_Type",
    "DM_Treatment", "Smoking_History", "Waist", "BMI", "Fasting_Blood_Glucose_Value_SI_Units",
    "HbA1C_Admission_Value", "Lipid_24_Collected", "Cholesterol_Value_SI_Units",
    "Triglycerides_Value_SI_Units", "Creatinine_Clearance", "Heart_Rate"
]
classifacation_methods = [
        {"method":"RF", "title":"Random Forest"},
        {"method":"ANN", "title":"Artificial Neural Network"},
        {"method":"SVM", "title":"Support Vector Machine"},
     ]    

tb = TableLogger(columns='method,Accuracy,Precision,Recall,F1_score',
                    default_colwidth=9,
                    float_format='{:,.2f}'.format)


for i in classifacation_methods :
    method = i["method"] 
    if method == "RF":
        model = RandomForestClassifier()
    elif method == "ANN":
        model = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=4000)
    else:
        model = SVC(kernel='rbf', C=1.0, gamma='auto')
    # Train the model on the training data
    df = pd.read_csv("csv/FinalResult_MI.csv", usecols=variables)
    # stocker tous les variables et sont valeur dans X sauf DM
    X = df.drop("DM", axis=1)
    # stocker les valeurs de DM dans y
    y = df["DM"]


    # diviser les données en ensembles d'apprentissage et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    #  normaliser les données d'apprentissage et de test
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    model.fit(X_train, y_train)

    # Entraînement du modèle
    y_pred = model.predict(X_test)


    # Évaluation du modèle
    tb(
    i["method"],
    "{:.2f}".format(accuracy_score(y_test, y_pred)*100) + " %", 
    "{:.2f}".format(recall_score(y_test, y_pred)*100) + " %",
    "{:.2f}".format(recall_score(y_test, y_pred)*100) + " %",
    "{:.2f}".format(f1_score(y_test, y_pred)*100)+ " %"
    )
    # Train the model on the training data
# fermer le tableau
tb.print_line(("+"+"-"*11)*5+"+")