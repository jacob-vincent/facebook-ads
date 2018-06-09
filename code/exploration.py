import pandas as pd
import numpy as np
import os
#Read in data
cwd=os.getcwd()
os.chdir(cwd+'/facebookads/data')

data_df = pd.read_csv('parsed_data.csv')
data_df.head()
