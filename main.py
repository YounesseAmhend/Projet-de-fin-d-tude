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

numeric_variables = [
    
                     'Age', 'Year_DM_Diagnosed', 'DM_Duration', 'Waist', 'BMI', 'Fasting_Blood_Glucose_Value_SI_Units',
                     'HbA1C_Admission_Value', 'Cholesterol_Value_SI_Units', 'Triglycerides_Value_SI_Units', 
                     'Creatinine_Clearance', 'Heart_Rate'
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
                df.loc[i, "Year_DM_Diagnosed"] = 2013 - float(df.loc[i, "Year_DM_Diagnosed"])
        
def clean(df, column:str, min:float, max:float, conv:float=1.0)->None:
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
            wrong_values.append({"id":i+2,"value":df[column][i],"min":min,"max":max, "conv":conv, "minConv":min/conv, "maxConv":max/conv})
            
    # printing result
    with open("variablesToClean.txt", "w") as f:
        f.close()
    with open("variablesToClean.txt", "a") as f:
        f.write("_________________________________________________________________________________________________________________________________________________________________\n")
        f.write(str(column)+" " +str(len(wrong_values))+"\n")
        f.write("_________________________________________________________________________________________________________________________________________________________________\n")
        for i in wrong_values:
            f.write(str(i)+"\n")

def fillValue(df, column:str, newValue:str)->None:
    df[column].fillna(newValue, inplace=True)



dfall = pd.read_csv("csv/Gulf.csv", low_memory=False, usecols = variables)


dfall.to_excel("Excel/Original.xlsx")
profile = ProfileReport(dfall)
profile.to_file("Analysis/Analysis.html")

# encodage
le = LabelEncoder()
encodingKey = []

for i in to_numeric:
    
    dfall[i] = le.fit_transform(dfall[i])
    key = dfall[i].unique()
    temp = []
    count = 0
    
    for row in dfall[i].unique():
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
profile = ProfileReport(dfall)
profile.to_file("Analysis/EncodedAnalysis.html")

# cleaning
cleanDm(dfall)
fillValue(df = dfall, column="DM_Type", newValue="Not sick")
fillValue(df = dfall, column="DM_Treatment", newValue="Not sick")

clean(df=dfall, column="Year_DM_Diagnosed", min=1967 ,max=2013,conv=1) 
clean(df=dfall, column="DM_Duration", min=0 ,max=45,conv=1)
clean(df=dfall, column="Heart_Rate", min=25 ,max=300,conv=1)
clean(df=dfall, column="HbA1C_Admission_Value", min=3.9 ,max=14.1,conv=1)
clean(df=dfall, column="Cholesterol_Value_SI_Units", min=1 ,max=25.86,conv=0.02586)
clean(df=dfall, column="Triglycerides_Value_SI_Units", min=0.2 ,max=22.58,conv=0.01129)
clean(df=dfall, column="BMI", min=9 ,max=105,conv=1)
clean(df=dfall, column="Creatinine_Clearance", min=5 ,max=200,conv=60)
clean(df=dfall, column="Fasting_Blood_Glucose_Value_SI_Units", min=1 ,max=20,conv=0.056)


dfall.to_excel("Excel/FinalResult.xlsx")
dfall.to_csv("csv/finalResult.csv")

dfall = pd.read_csv("csv/finalResult.csv", low_memory=False)


profile = ProfileReport(dfall)
profile.to_file("Analysis/FinalResult.html")


print("\n\n time :",time.process_time(), "s")

    
