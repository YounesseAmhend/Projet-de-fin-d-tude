import pandas as pd
from pandas_profiling import ProfileReport
import time
df = pd.read_csv("Gulf.csv", low_memory=False,usecols= [''])
profile = ProfileReport(df)
profile.to_file("Analysis.html")
profile.to_file("Analysis.json")
print("\n\n time :",time.process_time(), "s")

