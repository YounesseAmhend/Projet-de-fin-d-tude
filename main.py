import pandas as pd
from ydata_profiling import ProfileReport
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from missingpy import MissForest as MImputer



# une liste de variable qualitative 
to_num = [
    'Gender', 'Education', 'Work', 'Cardiac_Arrest_Admission', 'Non_Cardiac_Condition',
    'Hypertension', 'Dyslipidemia', 'DM', 'DM_Type', 'DM_Treatment', 'Smoking_History',
    'Lipid_24_Collected'
]

# une liste de tous les variables 
variables = [
    "Gender", "Age", "Education", "Work", "Cardiac_Arrest_Admission", "Non_Cardiac_Condition",
    "Hypertension",  "Dyslipidemia", "DM",  "DM_Type", "Year_DM_Diagnosed", "DM_Duration",
    "DM_Treatment", "Smoking_History", "Waist", "BMI", "Fasting_Blood_Glucose_Value_SI_Units",
    "HbA1C_Admission_Value", "Lipid_24_Collected", "Cholesterol_Value_SI_Units",
    "Triglycerides_Value_SI_Units", "Creatinine_Clearance", "Heart_Rate"
]
# une liste de variable quantitative 
numeric_variables = [
    "Year_DM_Diagnosed", "DM_Duration",
    'Age', 'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
    'HbA1C_Admission_Value', 'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units',
    'Creatinine_Clearance', 'Heart_Rate'
]
# une liste de variable qu'ils vont etre imputer 
variables_to_imput = [
    'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
    'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units',
    'Creatinine_Clearance', 'Heart_Rate', 'HbA1C_Admission_Value'
]
# une liste de variable qu'ils ne vont pas etre imputer 
variables_to_not_imput = []
for i in variables:
    if i not in variables_to_imput:
        variables_to_not_imput.append(i)


# cleaning functions
""" "-> 'type' ": le type de retourne (int, float, bool, str)
    "None" : le type de retourne est void (il ne retourne rien) """
    
def cleanDm(df) -> None:
    
    """ cette fonction remplir les champs qui manque soit Year_DM_Diagnosed ou DM_Duration
        mais pas les deux """
        
    for i in range(len(df["Year_DM_Diagnosed"])):
        
        if df["Year_DM_Diagnosed"][i] != df["Year_DM_Diagnosed"][i]: # verifier si la case de Year_DM_Diagnosed est vide("")
            if df["DM_Duration"][i] != df["DM_Duration"][i]: # verifier si la case de DM_Duration est vide
                continue  # si les deux sont vide, alors on va continue(squip)
            else: 
                df.loc[i, "Year_DM_Diagnosed"] = 2013 - float(df.loc[i, "DM_Duration"]) # 2013 c'est l'anneé dans lequel elle mesure la duration de diabete (DM_Duration)
        elif df["DM_Duration"][i] != df["DM_Duration"][i]: # verifier si la case de DM_Duration est vide("")
            if df["Year_DM_Diagnosed"][i] != df["Year_DM_Diagnosed"][i]: # verifier si la case de Year_DM_Diagnosed est vide
                continue # skip
            else:
                df.loc[i, "DM_Duration"] = 2013 - float(df.loc[i, "Year_DM_Diagnosed"]) # la duration = l'année courante(2013) - l'année de diabete

""" cette fonction unifier les unité (converter les variables) 
    et stocker les variable incorrect dans un fichier de text """
    
def clean(df, column: str, min: float, max: float, conv: float = 1.0) -> None:
    wrong_values = [] # la liste ou on va stocker les lignes quand doit etre netoyer
    for i in range(len(df[column])): # pour chaque ligne de la variable donné(column)
        if df[column][i] != df[column][i]: # verifier si la case est vide ("")
            continue # skip
        value = float(df[column][i]) # converter l'element a un float pour eviter les erreurs
        if min <= value and value <= max: # verifier si l'element est dans l'intervale normal
            continue # skip
        elif min <= (value*conv) and (value*conv) <= max: # verifier si l'element a une autre unite
            df.loc[i, column] = value*conv # converter l'element á l'unité standard
        elif df.loc[i, column] == 0: # verifier si l'element est 0 (il impossible d'avoir une variable qui a 0 dans cette base de donné)
            df.loc[i, column] = "" # vider l'element pour l'imputer aprés
        else: # # stoker les autres varibale pour les nettoyer
            wrong_values.append(
                {"id": i, "value": df[column][i], "min": min, "max": max, "minConv": min/conv, "maxConv": max/conv})

    # cree un fichier nomme 'variablesToClean.txt' pour afficher les variables á nettoyer
    with open("variablesToClean.txt", "a") as f:
        f.write("_________________________________________________________________________________________________________________________________________________________________\n")
        f.write(str(column)+" " + str(len(wrong_values))+"\n")
        f.write("_________________________________________________________________________________________________________________________________________________________________\n")
        for i in wrong_values:
            f.write(str(i)+"\n")

# importer tous la base de donne avec les columns qu'on a besoin dans dfall
dfall = pd.read_csv("csv/Gulf.csv", low_memory=False, usecols=variables)
# importer tous les variables á encoder
ds = pd.read_csv("csv/Gulf.csv", low_memory=False, usecols=to_num)


dfall.to_excel("Excel/Original.xlsx")

# faire les analyises

# profile = ProfileReport(dfall)

#afficher les analyises dans une page web

# profile.to_file("Analysis/Original.html")

cleanDm(dfall)

#juste pour eviter les erreurs
dfall.to_csv("csv/Mod.csv")
dfall = pd.read_csv("csv/Mod.csv", low_memory=False, usecols=variables)

# encodage
le = LabelEncoder()
encodingKey = []


for i in to_num:
    #encodage par chaque column 
    dfall[i] = pd.to_numeric(le.fit_transform(dfall[i].astype(str)))
    key = dfall[i].unique()
    temp = []
    count = 0
    # juste pour stocker les valeurs donné par la fonction de l'encodage
    for row in ds[i].unique():
        temp.append({f"{key[count]}": row})
        count += 1
    encodingKey.append({i: temp})



with open("encodingKey.json", "w") as f:
    f.write("[\n")
    for i in range(len(encodingKey)):
        if i != len(encodingKey)-1:
            f.write(str(encodingKey[i]).replace(
                "\'", "\"").replace("nan", "\"\"")+",\n")
        else:
            f.write(str(encodingKey[i]).replace(
                "\'", "\"").replace("nan", "\"\"")+"\n")
    f.write("]")
    f.close()
    
dfall.to_excel("Excel/Encoded.xlsx")
# profile = ProfileReport(dfall)
# profile.to_file("Analysis/EncodedAnalysis.html")

# cleaning

with open("variablesToClean.txt", "w") as f:
    f.close()

clean(df=dfall, column="Year_DM_Diagnosed", min=1967, max=2013, conv=1)
clean(df=dfall, column="DM_Duration", min=0, max=45, conv=1)
clean(df=dfall, column="Heart_Rate", min=25, max=300, conv=1)
clean(df=dfall, column="HbA1C_Admission_Value", min=1, max=100, conv=1)
clean(df=dfall, column="Cholesterol_Value_SI_Units", min=0.01, max=147.2, conv=0.02586)
clean(df=dfall, column="Triglycerides_Value_SI_Units", min=0.01, max=22.58, conv=0.0113)
clean(df=dfall, column="BMI", min=9.4, max=150, conv=1)
clean(df=dfall, column="Creatinine_Clearance", min=5, max=1200, conv=60)
clean(df=dfall, column="Fasting_Blood_Glucose_Value_SI_Units", min=0.3, max=17.8, conv=0.056)

# supprimer les lignes qui ont plus 25% des variables manquantes
dfall = dfall[ dfall.isna().mean(axis=1) <= 0.25 ]

dfall.to_excel("Excel/CleanedResult.xlsx", float_format="%.2f")
dfall.to_csv("csv/CleanedResult.csv")

# profile = ProfileReport(dfall, infer_dtypes=False, minimal=True)
# profile.to_file("Analysis/EncodedCleanedAnalysis.html")

dfall = pd.read_csv("csv/CleanedResult.csv", low_memory=False, usecols=variables_to_not_imput)
df_imput = pd.read_csv("csv/CleanedResult.csv", low_memory=False, usecols=variables_to_imput)


# Imputation

# KNN
imputer_KNN = KNNImputer(n_neighbors=5)
df_imputed_KNN = imputer_KNN.fit_transform(df_imput)

df_imput_KNN = pd.DataFrame(df_imputed_KNN, columns=df_imput.columns)
dfall_KNN = dfall.merge(df_imput_KNN, left_index=True, right_index=True)

df_imput_KNN.to_excel("Excel/imputed_KNN.xlsx")
dfall_KNN.to_excel("Excel/FinalResult_KNN.xlsx")
dfall_KNN.to_csv("csv/FinalResult_KNN.csv", float_format="%.2f")


# MI
imputer_MI = MImputer()
df_imputed_MI = imputer_MI.fit_transform(df_imput)

df_imput_MI = pd.DataFrame(df_imputed_MI, columns=df_imput.columns)
dfall_MI = dfall.merge(df_imput_MI, left_index=True, right_index=True)

df_imput_MI.to_excel("Excel/imputed_MI.xlsx")
dfall_MI.to_excel("Excel/FinalResult_MI.xlsx")
dfall_MI.to_csv("csv/FinalResult_MI.csv", float_format="%.2f")

# KNN
profile = ProfileReport(dfall_KNN, infer_dtypes=False, minimal=True)
profile.to_file("Analysis/FinalResult_KNN.html")

profile = ProfileReport(dfall_KNN, infer_dtypes=False, lazy=False)
profile.to_file("Analysis/FullFinalResult_KNN.html")

# MI
profile = ProfileReport(dfall_MI, infer_dtypes=False, minimal=True)
profile.to_file("Analysis/FinalResult_MI.html")

profile = ProfileReport(dfall_MI, infer_dtypes=False,  lazy=False)
profile.to_file("Analysis/FullFinalResult_MI.html")
