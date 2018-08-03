import pandas as pd
import numpy as np
import nltk as nltk
import os
from datetime import datetime as dt
import collections

#Read in data
# os.chdir('../data')
data_path = '../data/parsed_data.csv'
data_df = pd.read_csv(data_path)

#Make all column names lower case for simplicity
new_names = {}
for item in data_df.columns:
    new_names[item]=item.lower()

data_df.rename(columns=new_names,inplace=True)

#function to convert entries in "creationdate" column to datetime objects
def convert_time(item):
    if type(item)==str:
        return dt.strptime(item[:-4],'%m/%d/%y %I:%M:%S %p')
    else:
        return np.nan

#This dictionary will fix all of the typographical errors in the "creationdate" column
creation_date_errors = {'02/18/1605:12:00 AM PST':'02/18/16 05:12:00 AM PST', '03/22/1607:17:38 AM PDT':'03/22/16 07:17:38 AM PDT', '04/13/1607:31:13 AM PDT':'04/13/16 07:31:13 AM PDT', '10/20/16 07:51:40AM PDT':'10/20/16 07:51:40 AM PDT', '11/03/1608:21:10 AM PST':'11/03/16 08:21:10 AM PST', '11/10/1607:17:06 AM PST':'11/10/16 07:17:06 AM PST', '11/01/16 03:03:08 AM P':'11/01/16 03:03:08 AM PST', '11/01/16 08:03:20 AM P':'11/01/16 08:03:20 AM PST', '11/01/16 08:04:40 AM PST':'11/01/16 08:04:40 AM PST', '12/07/1611:37:56 PM PST':'12/07/16 11:37:56 PM PST', '12/08/1606:22:13 AM PST':'12/08/16 06:22:13 AM PST', '12/27/1611:32:51 PM PST':'12/27/16 11:32:51 PM PST', '05/16/1706:17:51 AM PDT':'05/16/17 06:17:51 AM PDT', '05/17/17 04:21:04AM PDT':'05/17/17 04:21:04 AM PDT', '02/07/1707:18:42 AM PST':'02/07/17 07:18:42 AM PST', '02/06/1707:17:41 AM PST':'02/06/17 07:17:41 AM PST', '03/14/17 07:01:00AM PDT':'03/14/17 07:01:00 AM PDT'}

#This dicitonary will fix the errors found in the "enddate" column
end_date_errors = {'07/11/1505:36:03AM PDT':'07/11/15 05:36:03 AM PDT',
                   '07/11/1507:00:00AM PDT':'07/11/15 07:00:00 AM PDT',
                   '11/10/1607:21:10 AM PST':'11/10/16 07:21:10 AM PST',
                   '12/08/1611:37:56 PM PST':'12/08/16 11:37:56 PM PST',
                   '12/09/1606:22:13 AM PST':'12/09/16 06:22:13 AM PST',
                   '01/27/17 01:29:39AM PST':'01/27/17 01:29:39 AM PST',
                   '03/30/17 07:31:03AM PDT':'03/30/17 07:31:03 AM PDT'}

#Fix the errors in the "creationdate" column
for item in data_df['creationdate']:
    if item in creation_date_errors:
        data_df['creationdate'] = creation_date_errors[item]
    else:
        data_df['creationdate'] = data_df['creationdate']

#Fix the errors in the "enddate" column
for item in data_df['enddate']:
    if item in end_date_errors:
        data_df['enddate'] = end_date_errors[item]
    else:
        data_df['enddate'] = data_df['enddate']

#Convert all entries to datetime objects
data_df['creation_date_time'] = data_df['creationdate'].map(convert_time)
data_df['end_date_time'] = data_df['enddate'].map(convert_time)
data_df.drop(['creationdate','enddate'],axis=1,inplace=True)

# Determine amount of missing data in each columns
# If more than 2/3 of a column's entires are NaN, then we drop that column
for item in data_df.columns:
    nulls = data_df[item].isnull().sum()
    missing = round(nulls*1.0/data_df.shape[0]*100,2)
    #if missing > 10:
        #print("{} has {} null values ({}%)".format(item,nulls,missing))
    if missing > 2/3*100:
        data_df = data_df.drop(item, axis=1)
        print('Dropped {} due to incompleteness ({}% missing)'.format(item.upper(),missing))
print('\n ------------ \n')
#Function to tokenize the ad text and remove punctuation
def text_cleaner(text):
    # print(type(text))
    new_words = []
    stop_words = nltk.corpus.stopwords.words('english')
    if type(text) == str:
        # print('Cleaning...')
        for item in nltk.word_tokenize(text):
            if item not in stop_words and item.isalnum():
                new_words.append(item)
        return new_words
    else:
        # print('Not a string')
        return np.nan

#Clean the ad text entries and drop the original column
data_df['clean_text'] = data_df['adtext'].map(text_cleaner)
# data_df.drop('adtext',axis=1,inplace=True)

#Function to grab the lower bound of the age range
def min_age(cell):
    return cell[0:2]

#Function to grab the upper bound of the age range (note that some ranges end in "+")
def max_age(cell):
    if cell[-1] == '+':
        return int(cell[-3:-1])
    else:
        return int(cell[-2:])

#Grab lower and upper bounds of the age ranges and cast them as numeric values
data_df['age_lower'] = pd.to_numeric(data_df['age'].map(min_age))
data_df['age_upper'] = pd.to_numeric(data_df['age'].map(max_age))
data_df.drop('age',axis=1,inplace=True)

print('data_df currently has '+str(data_df.shape[0])+' rows and '+str(data_df.shape[1])+' columns')
print('\n ------------ \n')

def term_frequency(col):
    token = nltk.word_tokenize(col)
    text = []
    for item in token:
        if item.isalnum():
            text.append(item)
        else:
            continue
    freqs = collections.Counter(text)
    return freqs

# term_frequency(data_df['adtext'][321])


#Concatenate list of all ad texts
texts = []
for item in data_df['adtext']:
    texts.append(item)


#Tokenize the corpus of texts and grab word frequencies
texts_tokens = []
for i in texts:
    if type(i)==str:
        result = nltk.word_tokenize(i)
        for r in result:
            if r.isalnum():
                texts_tokens.append(r)
    else:
        continue

texts_tokens_freqs = dict(collections.Counter(texts_tokens))


sorted_text_token_freqs = sorted(texts_tokens_freqs.items(), key=lambda kv: kv[1],reverse=True)

idf = np.empty(len(sorted_text_token_freqs),dtype=np.float)
for i in range(len(idf)):
    idf[i]=data_df.shape[0]/(np.log(sorted_text_token_freqs[i][1]))#this is wrong. should be number of documents containing word i
# idf[0:10]

sorted_dict_freqs = dict(sorted_text_token_freqs)

term_list = list(zip(sorted_dict_freqs.keys(),sorted_dict_freqs.values(),idf))


term_tfidf = list()
for item in term_list:
    term_tfidf.append([item[0],item[1]*(data_df.shape[0]/np.log(item[2]])))
print(term_tfidf[0:5])
