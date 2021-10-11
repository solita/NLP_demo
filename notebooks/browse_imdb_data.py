import os
import pandas as pd
import numpy as np

data_dir = '/home/ml_user/data/IMDb_raw'

# Read titles:
file_name = os.path.join(data_dir, 'title.akas.tsv')
df_titles = pd.read_csv(file_name, sep='\t')

# Read references to negative reviews for training data:
file_name = os.path.join(data_dir, 'aclImdb/train/urls_neg.txt')

myclient = pymongo.MongoClient("mongodb://NLP_mongo:27017/")
mydb = myclient["movies"]
mycol = mydb["titles"]

df_uniq_titles = df_titles.titleId.drop_duplicates()

for ind in range(0,10):
    print(df_uniq_titles.iloc[ind])

    df_title = df_titles.loc[df_titles.titleId == df_uniq_titles.iloc[ind]].copy()

    df_title = df_title.replace('\\N', '')

    orig_title_list = df_title.loc[df_title.isOriginalTitle == 1, 'title'].to_list()
    orig_title_lang_list = df_title.loc[df_title.isOriginalTitle == 1, 'language'].to_list()

    if len(orig_title_list) > 0:
        orig_title = orig_title_list[0]
        orig_title_lang = orig_title_lang_list[0]

    alt_title_list = df_title.loc[df_title.isOriginalTitle == 0, 'title'].to_list()
    alt_title_lang_list = df_title.loc[df_title.isOriginalTitle == 0, 'language'].to_list()

    imdb_id = df_title.titleId[0]

    insert_dict = {'imdb_id': imdb_id, 'orig_title': orig_title, 'orig_title_lang': orig_title_lang, 'alternate_titles': alt_title_list, 'alternate_title_lang': alt_title_lang_list}

    print(insert_dict)

    mycol.insert_one(insert_dict)


df_train_neg_urls = pd.read_csv(file_name, sep='\s+', header=None)

print('Number of urls (train, neg): %d' % len(df_train_neg_urls))

file_list = []
review_ind_list = []
review_score_list = []
review_text = []

for root, dirs, files in os.walk(os.path.join(data_dir, 'aclImdb/train/neg')):
    for file_name in files:
        if file_name.endswith('.txt'):
            file_list.append(os.path.join(root, file_name))
            file_name_body = os.path.splitext(file_name)[0]
            review_ind_list.append(file_name_body.split('_')[0])
            review_score_list.append(file_name_body.split('_')[1])

            with open(file_list[-1]) as fh:
                lines = fh.readlines()[0]

            review_text.append(lines)

print('Number of review texts (train, neg): %d' % len(file_list))

print(df_train_neg_urls.head())

df_train_ind_refs = pd.DataFrame({'ind': review_ind_list, 'score': review_score_list, 'text': review_text})

# Update types:
df_train_ind_refs.ind = df_train_ind_refs.ind.astype('int')
df_train_ind_refs.score = df_train_ind_refs.score.astype('int')

df_train_ind_refs.sort_values(by=['ind'], inplace=True, ignore_index=True)

print(df_train_ind_refs.head())

print(df_train_ind_refs.iloc[0,2])

