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
             "HbA1C_Admission_Value" , "Lipid_24_Collected" , "Cholesterol_Value_SI_Units" , 
             "Triglycerides_Value_SI_Units","Creatinine_Clearance", "Heart_Rate"
             ]

numeric_variables = ['Age', 'Year_DM_Diagnosed', 'DM_Duration', 'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
                     'HbA1C_Admission_Value', 'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units', 
                     'Creatinine_Clearance', 'Heart_Rate'
                     ]
# cleaning functions

def clean(df, column:str, min:float, max:float, conv:float=1.0):
    wrong_values = []
    for i in range(len(df[column])):
        if df[column][i]=="" or df[column][i]!=df[column][i]:
            continue
        value = float(df[column][i])
        if min <= value and value <= max:
            continue
        elif  min <= (value*conv) and (value*conv )<= max:
            df.loc[i, column]=value*conv
        else:
            wrong_values.append({"id":i+2,"value":df[column][i],"min":min,"max":max, "conv":conv, "minConv":min/conv, "maxConv":max/conv})
    print("______________________________________________________________________________________________________________")
    print(column, len(wrong_values))
    
    for i in wrong_values:
        print(i,"\n")
def replaceValue(df, column:str, newValue:str, valueToReplace:str):
    df[column] = df[column].replace(valueToReplace, value)

df = pd.read_csv("Gulf.csv", low_memory=False, usecols=numeric_variables)
ds = pd.read_csv("Gulf.csv", low_memory=False, usecols=to_numeric)
dfall = pd.read_csv("Gulf.csv", low_memory=False, usecols=variables)

ohe = LabelEncoder()

numeric = ds.apply(ohe.fit_transform)
# feature_labels = ohe.categories_
# feature_labels = np.concatenate(feature_labels, dtype=object)



# dp = pd.DataFrame(feature_array,columns=feature_labels)

dl = df.merge(numeric,left_index=True, right_index=True)
dl.to_excel("results.xlsx")
dfall.to_excel("old.xlsx")

profile = ProfileReport(dall)
profile.to_file("AnalysisAll.html")
profile = ProfileReport(dl)
profile.to_file("encodedAnalysis.html")

# cleaning
clean(df=dfall, column="Year_DM_Diagnosed", min=1967 ,max=2013,conv=1) 
clean(df=dfall, column="DM_Duration", min=0 ,max=45,conv=1)
clean(df=dfall, column="Heart_Rate", min=25 ,max=300,conv=1)
clean(df=dfall, column="HbA1C_Admission_Value", min=3.9 ,max=14.1,conv=1)
clean(df=dfall, column="Cholesterol_Value_SI_Units", min=1 ,max=25.86,conv=0.02586)
clean(df=dfall, column="Triglycerides_Value_SI_Units", min=0.2 ,max=22.58,conv=0.01129)
clean(df=dfall, column="BMI", min=9 ,max=105,conv=1)
clean(df=dfall, column="Creatinine_Clearance", min=5 ,max=200,conv=60)
clean(df=dfall, column="Fasting_Blood_Glucose_Value_SI_Units", min=1 ,max=20,conv=0.056)

clean(df=dl, column="Year_DM_Diagnosed", min=1967 ,max=2013,conv=1)
clean(df=dl, column="DM_Duration", min=0 ,max=45,conv=1)
clean(df=dl, column="Heart_Rate", min=25 ,max=300,conv=1)
clean(df=dl, column="HbA1C_Admission_Value", min=3.9 ,max=14.1,conv=1)
clean(df=dl, column="Cholesterol_Value_SI_Units", min=1 ,max=25.86,conv=0.02586)
clean(df=dl, column="Triglycerides_Value_SI_Units", min=0.2 ,max=22.58,conv=0.01129)
clean(df=dl, column="BMI", min=9 ,max=105,conv=1)
clean(df=dl, column="Creatinine_Clearance", min=5 ,max=200,conv=60)
clean(df=dl, column="Fasting_Blood_Glucose_Value_SI_Units", min=1 ,max=20,conv=0.056)

dl.to_excel("resultsCleaned.xlsx")
dl.to_csv("resultsCleaned.csv")
dfall.to_excel("oldCleaned.xlsx")
dfall.to_csv("oldCleaned.csv")

dfall = pd.read_csv("oldCleaned.csv", low_memory=False, usecols=variables)
dl = pd.read_csv("resultsCleaned.csv", low_memory=False, usecols=variables)

profile = ProfileReport(dfall)
profile.to_file("AnalysisAllCleaned.html")
profile = ProfileReport(dl)
profile.to_file("encodedAnalysisCleaned.html")


print("\n\n time :",time.process_time(), "s")

    
