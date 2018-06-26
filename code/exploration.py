import pandas as pd
import numpy as np
import nltk as nltk
import os
from datetime import datetime as dt

#Read in data
cwd=os.getcwd()
os.chdir(cwd+'/data')

data_df = pd.read_csv('parsed_data.csv')
# data_df.head()

new_names = {}
for item in data_df.columns:
    new_names[item]=item.lower()

data_df.rename(columns=new_names,inplace=True)

print(data_df['creationdate'][0])
print(dt.strptime(data_df['creationdate'][0][:-4], '%m/%d/%y %I:%M:%S %p'))

def convert_time(item):
    if type(item)==str:
        return dt.strptime(item[:-4],'%m/%d/%y %I:%M:%S %p')
    else:
        return np.nan

print(convert_time(data_df['creationdate'][0]))
type(convert_time(data_df['creationdate'][0]))
type(data_df['creationdate'][0])
fix_these = {'02/18/1605:12:00 AM PST':'02/18/16 05:12:00 AM PST', '03/22/1607:17:38 AM PDT':'03/22/16 07:17:38 AM PDT', '04/13/1607:31:13 AM PDT':'04/13/16 07:31:13 AM PDT', '10/20/16 07:51:40AM PDT':'10/20/16 07:51:40 AM PDT', '11/03/1608:21:10 AM PST':'11/03/16 08:21:10 AM PST', '11/10/1607:17:06 AM PST':'11/10/16 07:17:06 AM PST', '11/01/16 03:03:08 AM P':'11/01/16 03:03:08 AM PST', '11/01/16 08:03:20 AM P':'11/01/16 08:03:20 AM PST', '11/01/16 08:04:40 AM PST':'11/01/16 08:04:40 AM PST', '12/07/1611:37:56 PM PST':'12/07/16 11:37:56 PM PST', '12/08/1606:22:13 AM PST':'12/08/16 06:22:13 AM PST', '12/27/1611:32:51 PM PST':'12/27/16 11:32:51 PM PST', '05/16/1706:17:51 AM PDT':'05/16/17 06:17:51 AM PDT', '05/17/17 04:21:04AM PDT':'05/17/17 04:21:04 AM PDT', '02/07/1707:18:42 AM PST':'02/07/17 07:18:42 AM PST', '02/06/1707:17:41 AM PST':'02/06/17 07:17:41 AM PST', '03/14/17 07:01:00AM PDT':'03/14/17 07:01:00 AM PDT'}

fix_these['02/18/1605:12:00 AM PST']

for item in data_df['creationdate']:
    if item in fix_these:
        data_df['creationdate'] = fix_these[item]
    else:
        data_df['creationdate'] = data_df['creationdate']

data_df['date_time'] = data_df['creationdate'].map(convert_time)
# data_df.head()

# Determine amount of missing data in each columns
# If more than 50% of a columns entires are NaN, then we drop that column
for item in data_df.columns:
    nulls = data_df[item].isnull().sum()
    missing = round(nulls*1.0/data_df.shape[0]*100,2)
    if missing > 10:
        print("{} has {} null values ({}%)".format(item,nulls,missing))
    # if missing > 50:
        # data_df = data_df.drop(item, axis=1)
data_df.shape

def text_cleaner(text):
    # print(type(text))
    new_words = []
    stop_words = nltk.corpus.stopwords.words('english')
    if type(text) == str:
        # print('Cleaning...')
        for item in nltk.word_tokenize(text):
            if item not in stop_words:
                new_words.append(item)
        return new_words
    else:
        # print('Not a string')
        return np.nan

data_df['clean_text'] = data_df['adtext'].map(text_cleaner)
data_df['clean_text'].head()
