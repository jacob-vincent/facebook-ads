import pandas as pd
import numpy as np
import os
from datetime import datetime as dt

os.getcwd()
data_df = pd.read_csv('/Users/jvincen7/Downloads/FacebookAds.csv')
data_df.head()
data_df.shape

data_df['Age'].unique()
data_df['CreationDate'][0][:-4]
type(data_df['CreationDate'][0])
print(dt.strptime('06/10/15 02:59:53 AM', "%m/%d/%y %I:%M:%S %p"))

print(dt.strptime(data_df['CreationDate'][0][:-4],"%m/%d/%y %I:%M:%S %p"))
