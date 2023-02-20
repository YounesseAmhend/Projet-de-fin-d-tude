import pandas as pd
from pandas_profiling import ProfileReport
import time

def cleanSpecial(df):
    # supprimer les caractères speciaux (*&^£@~#!*^%") dans les columns donnees
    for column in df.columns:
        df[column] = df[column].str.replace(r"\W", "")
    # cree nouveau fichier pour afficher les resultas
    df.to_csv("results.csv")
    
df = pd.read_csv("Gulf.csv", low_memory=False,usecols= ['Hospital'])
profile = ProfileReport(df)
profile.to_file("Analysis.html")
profile.to_file("Analysis.json")
# cleanSpecial(df) test
print("\n\n time :",time.process_time(), "s")

    
