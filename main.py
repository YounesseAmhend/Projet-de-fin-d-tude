import pandas as pd
from ydata_profiling import ProfileReport
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import np
import time


to_numeric = [
              'Gender', 'Education', 'Work', 'Cardiac_Arrest_Admission', 'Non_Cardiac_Condition',
              'Hypertension', 'Dyslipidemia', 'DM', 'DM_Type', 'DM_Treatment', 'Smoking_History',
              'Lipid_24_Collected'
              ]

variables = [
             "Gender", "Age", "Education", "Work", "Cardiac_Arrest_Admission", "Non_Cardiac_Condition",
             "Hypertension" ,  "Dyslipidemia" , "DM" , "Year_DM_Diagnosed" , "DM_Duration" , "DM_Type",
             "DM_Treatment" , "Smoking_History" , "Waist" , "BMI"  , "Fasting_Blood_Glucose_Value_SI_Units",
             "HbA1C_Admission_Value" , "Lipid_24_Collected" , "Cholesterol_Value_SI_Units" , 
             "Triglycerides_Value_SI_Units","Creatinine_Clearance", "Heart_Rate"
             ]
numeric_variables = [
    
                     'Age', 'Year_DM_Diagnosed', 'DM_Duration', 'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
                     'HbA1C_Admission_Value', 'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units', 
                     'Creatinine_Clearance', 'Heart_Rate'
                     ]

variables_to_imput = [
                       'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
                      'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units', 
                     'Creatinine_Clearance', 'Heart_Rate'   
]
variables_to_not_imput = [
    'Gender', 'Age', 'Education', 'Work', 'Cardiac_Arrest_Admission', 'Non_Cardiac_Condition', 
    'Hypertension', 'Dyslipidemia', 'DM', 'Year_DM_Diagnosed', 'DM_Duration', 'DM_Type', 'DM_Treatment',
    'Smoking_History', 'HbA1C_Admission_Value', 'Lipid_24_Collected'
]


# cleaning functions
def cleanDm(df)->None:
    for i in range(len(df["Year_DM_Diagnosed"])):
        if df["Year_DM_Diagnosed"][i]!=df["Year_DM_Diagnosed"][i]:
            if df["DM_Duration"][i]!=df["DM_Duration"][i]:
                continue
            else:
                df.loc[i, "Year_DM_Diagnosed"] = 2013 - float(df.loc[i, "DM_Duration"])
        elif df["DM_Duration"][i]!=df["DM_Duration"][i]:
            if df["Year_DM_Diagnosed"][i]!=df["Year_DM_Diagnosed"][i]:
                continue
            else:
                df.loc[i, "DM_Duration"] = 2013 - float(df.loc[i, "Year_DM_Diagnosed"])
                
def clean(df, column:str, min:float, max:float, conv:float=1.0) -> None:
    wrong_values = []
    for i in range(len(df[column])):
        if df[column][i]!=df[column][i]:
            continue
        value = float(df[column][i])
        if min <= value and value <= max:
            continue
        elif  min <= (value*conv) and (value*conv )<= max:
            df.loc[i, column]=value*conv
        else:
            wrong_values.append({"id":i+2,"value":df[column][i],"min":min,"max":max,"minConv":min/conv, "maxConv":max/conv})
            
    # printing result
    with open("variablesToClean.txt", "a") as f:
        f.write("_________________________________________________________________________________________________________________________________________________________________\n")
        f.write(str(column)+" " +str(len(wrong_values))+"\n")
        f.write("_________________________________________________________________________________________________________________________________________________________________\n")
        for i in wrong_values:
            f.write(str(i)+"\n")

def fillValue(df, column:str, newValue:str) -> None:
    df[column].fillna(newValue, inplace=True)



dfall = pd.read_csv("csv/Gulf.csv", low_memory=False, usecols = variables)
ds = pd.read_csv("csv/Gulf.csv", low_memory=False, usecols = to_numeric)
df_imput = pd.read_csv("csv/Gulf.csv", low_memory=False, usecols = variables_to_imput)

dfall.to_excel("Excel/Original.xlsx")
# profile = ProfileReport(dfall)
# profile.to_file("Analysis/Analysis.html")

cleanDm(dfall)
fillValue(dfall, "DM_Type", "Not sick")
fillValue(dfall, "DM_Treatment", "Not sick")

# encodage
le = LabelEncoder()
encodingKey = []

for i in to_numeric:
    
    dfall[i] = pd.to_numeric(le.fit_transform(dfall[i]))
    key = dfall[i].unique()
    temp = []
    count = 0
    
    for row in ds[i].unique():
        temp.append({f"{key[count]}": row})
        count+=1
        
    encodingKey.append({i: temp})
    
with open("encodingKey.json", "w") as f:
    f.write("[\n")
    for i in range(len(encodingKey)):
        if i != len(encodingKey)-1:
            f.write(str(encodingKey[i]).replace("\'","\"").replace("nan","\"\"")+",\n")
        else:
            f.write(str(encodingKey[i]).replace("\'","\"").replace("nan","\"\"")+"\n")
    f.write("]")
    f.close()

dfall.to_excel("Excel/Encoded.xlsx")
# profile = ProfileReport(dfall)
# profile.to_file("Analysis/EncodedAnalysis.html")

# cleaning

with open("variablesToClean.txt", "w") as f:
    f.close()
clean(df=dfall, column="Year_DM_Diagnosed", min=1967 ,max=2013,conv=1) 
clean(df=dfall, column="DM_Duration", min=0 ,max=45,conv=1)
clean(df=dfall, column="Heart_Rate", min=25 ,max=300,conv=1)
clean(df=dfall, column="HbA1C_Admission_Value", min=3.9 ,max=20,conv=1)
clean(df=dfall, column="Cholesterol_Value_SI_Units", min=1 ,max=25.86,conv=0.02586)
clean(df=dfall, column="Triglycerides_Value_SI_Units", min=0.2 ,max=22.58,conv=0.0113)
clean(df=dfall, column="BMI", min=9 ,max=105,conv=1)
clean(df=dfall, column="Creatinine_Clearance", min=5 ,max=1200,conv=60)
clean(df=dfall, column="Fasting_Blood_Glucose_Value_SI_Units", min=1 ,max=17.8,conv=0.056)


dfall.to_excel("Excel/CleanedResult.xlsx", float_format="%.2f")
dfall.to_csv("csv/CleanedResult.csv")

dfall = pd.read_csv("csv/CleanedResult.csv", low_memory=False)


# Impute missing values using MICE imputer
imputer = IterativeImputer()
df_imputed = imputer.fit_transform(df_imput)

# Convert imputed array back to DataFrame
df_imput = pd.DataFrame(df_imputed, columns=df_imput.columns)

dfall = pd.read_csv("csv/CleanedResult.csv", low_memory=False, usecols = variables_to_not_imput)
dfall =  dfall.merge(df_imput,left_index=True, right_index=True)

# for col in dfall:
#     dfall[col] = dfall[col].astype(float)

df_imput.to_excel("Excel/imputed.xlsx")
dfall.to_excel("Excel/FinalResult.xlsx")
dfall.to_csv("csv/finalResult.csv", float_format="%.2f")

dfall = pd.read_csv("csv/finalResult.csv", low_memory=False, usecols=variables)


profile = ProfileReport(dfall, infer_dtypes=False)
profile.to_file("Analysis/FinalResult.html")


print("\n\n time :",time.process_time(), "s")

    
