import pandas as pd
from ydata_profiling import ProfileReport
from sklearn.preprocessing import LabelEncoder
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
             "HbA1C_Admission_Value" , "Lipid_24_Collected" , "Cholesterol_Value_SI_Units" , "Triglycerides_Value_SI_Units",
             "Creatinine_Clearance", "Heart_Rate"
             ]

numeric_variables = ['Age', 'Year_DM_Diagnosed', 'DM_Duration', 'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
                     'HbA1C_Admission_Value', 'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units', 
                     'Creatinine_Clearance', 'Heart_Rate'
                     ]
def clean(df, column:str, min:float, max:float, conv:float=1.0):
    for i in range(len(df[column])):
        value = float(df[column][i])
        if min <= value and value <= max:
            continue
        elif  min <= (value*conv) and (value*conv )<= max:
            df.loc[i, column]=str(value*conv)
        else:
            df.loc[i, column]=""
def replaceValue(df, column:str, newValue:str, valueToReplace:str):
    df[column] = df[column].replace(valueToReplace, value)

df = pd.read_csv("Gulf.csv", low_memory=False, usecols=numeric_variables)
ds = pd.read_csv("Gulf.csv", low_memory=False, usecols=to_numeric)
dall = pd.read_csv("Gulf.csv", low_memory=False, usecols=variables)
        
print(type(dall["Age"][1]))
ohe = LabelEncoder()

numeric = ds.apply(ohe.fit_transform)
# feature_labels = ohe.categories_
# feature_labels = np.concatenate(feature_labels, dtype=object)



# dp = pd.DataFrame(feature_array,columns=feature_labels)

dl = df.merge(numeric,left_index=True, right_index=True)
dl.to_excel("results.xlsx")
clean(dall, column="Age", min=30, max=60)
dall.to_excel("old.xlsx")
profile = ProfileReport(dall)
profile.to_file("Analysis.html")
profile.to_file("Analysis.json")
profile = ProfileReport(dl)
profile.to_file("dl.html")

print("\n\n time :",time.process_time(), "s")

    
