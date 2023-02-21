import pandas as pd
from ydata_profiling import ProfileReport
import time

def cleanSpecial(df):
    # supprimer les caractères speciaux (*&^£@~#!*^%") dans les columns donnees
    #for column in df.columns:
    #    df[column] = df[column].str.replace(r"\W", "")
    # cree nouveau fichier pour afficher les resultas
    df.to_excel("results.xlsx")

variables = [
             "Gender", "Age", "Education", "Work", "Cardiac_Arrest_Admission", "Non_Cardiac_Condition",
             "Hypertension" ,  "Dyslipidemia" , "DM" , "Year_DM_Diagnosed" , "DM_Duration" , "DM_Type",
             "DM_Treatment" , "Smoking_History" , "Waist" , "BMI"  , "Fasting_Blood_Glucose_Value_SI_Units",
             "HbA1C_Admission_Value" , "Lipid_24_Collected" , "Cholesterol_Value_SI_Units" , "Triglycerides_Value_SI_Units",
             "Creatinine_Clearance", "Heart_Rate"
             ]

df = pd.read_csv("Gulf.csv", low_memory=False, usecols=variables)
profile = ProfileReport(df)

profile.to_file("Analysis.html")
profile.to_file("Analysis.json")

cleanSpecial(df)
print("\n\n time :",time.process_time(), "s")

    
