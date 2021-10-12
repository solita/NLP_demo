import os
import pandas as pd
import numpy as np
import pymongo

from tqdm import tqdm, trange

data_dir = '/home/ml_user/data/IMDb_raw'

##############################################################################

def get_review_param(base_dir, review_dir, url_file_name):

    # Read references to negative reviews for training data:
    file_name = os.path.join(base_dir, url_file_name)

    df_urls = pd.read_csv(file_name, sep='\s+', header=None)
    df_urls.columns = ['urls']
    df_urls['ind'] = df_urls.index.values
    df_urls['imdb_id'] = df_urls.urls.str.slice(26,35)

    # Read review texts:
    file_list = []
    review_ind_list = []
    review_score_list = []
    review_text = []

    for root, dirs, files in os.walk(os.path.join(data_dir, review_dir)):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_list.append(os.path.join(root, file_name))
                file_name_body = os.path.splitext(file_name)[0]
                review_ind_list.append(file_name_body.split('_')[0])
                review_score_list.append(file_name_body.split('_')[1])

                with open(file_list[-1]) as fh:
                    lines = fh.readlines()[0]

                review_text.append(lines)

    df_reviews = pd.DataFrame({'ind': review_ind_list, 'score': review_score_list, 'text': review_text})

    # Update types:
    df_reviews.ind = df_reviews.ind.astype('int')
    df_reviews.score = df_reviews.score.astype('int')

    # Sort:
    df_reviews.sort_values(by=['ind'], inplace=True, ignore_index=True)

    return df_reviews.merge(df_urls, how='left', on='ind')

##############################################################################

if __name__ == '__main__':

    # Get dataframes from raw text files:

    df_tr_neg = get_review_param(data_dir, 'aclImdb/train/neg', 'aclImdb/train/urls_neg.txt')
    df_tr_pos = get_review_param(data_dir, 'aclImdb/train/pos', 'aclImdb/train/urls_pos.txt')
    df_tr_unsup = get_review_param(data_dir, 'aclImdb/train/unsup', 'aclImdb/train/urls_unsup.txt')

    df_te_neg = get_review_param(data_dir, 'aclImdb/test/neg', 'aclImdb/test/urls_neg.txt')
    df_te_pos = get_review_param(data_dir, 'aclImdb/test/neg', 'aclImdb/test/urls_pos.txt')

    df_reviews_all = pd.concat([df_tr_neg, df_tr_pos, df_tr_unsup, df_te_neg, df_te_pos])

    df_reviews_all.sort_values(by=['imdb_id'], inplace=True, ignore_index=True)

    del df_tr_neg, df_tr_pos, df_tr_unsup, df_te_neg, df_te_pos

    df_uniq_titles = df_reviews_all.imdb_id.drop_duplicates()

    # Read titles:
    file_name = os.path.join(data_dir, 'title.akas.tsv')
    df_titles = pd.read_csv(file_name, sep='\t')
    df_titles = df_titles[df_titles.titleId.isin(df_uniq_titles)]

    # Read basics:
    # file_name = os.path.join(data_dir, 'title.basics.tsv')
    # df_basics = pd.read_csv(file_name, sep='\t')
    # df_basics = df_basics[df_basics.tconst.isin(df_uniq_titles)]

    # Read crew:
    # file_name = os.path.join(data_dir, 'title.crew.tsv')
    # df_crew = pd.read_csv(file_name, sep='\t')
    # df_crew = df_crew[df_crew.titleId.isin(df_uniq_titles)]

    # Read names:
    file_name = os.path.join(data_dir, 'name.basics.tsv')
    df_names = pd.read_csv(file_name, sep='\t')
    df_names['nconst_ind'] = df_names.nconst.str.slice(2,9)
    df_names['nconst_ind'] = df_names['nconst_ind'].astype('int')

    # Read principals:
    file_name = os.path.join(data_dir, 'title.principals.tsv')
    df_principals = pd.read_csv(file_name, sep='\t')
    df_principals = df_principals[df_principals.tconst.isin(df_uniq_titles)]
    df_principals['nconst_ind'] = df_principals.nconst.str.slice(2,9)
    df_principals['nconst_ind'] = df_principals['nconst_ind'].astype('int')

    print('Reading data complete.')

    # Connect to MongoDB.
    myclient = pymongo.MongoClient("mongodb://NLP_mongo:27017/")
    mydb = myclient["movies"]
    mycol = mydb["titles"]

    for ind in trange(len(df_uniq_titles)):
        title = df_uniq_titles.iloc[ind]

        # Rip titles:

        df_title = df_titles.loc[df_titles.titleId == title].copy()
        df_title = df_title.replace('\\N', '')

        orig_title_list = df_title.loc[df_title.isOriginalTitle == 1, 'title'].to_list()
        orig_title_lang_list = df_title.loc[df_title.isOriginalTitle == 1, 'language'].to_list()

        if len(orig_title_list) > 0:
            orig_title = orig_title_list[0]
            orig_title_lang = orig_title_lang_list[0]

        alt_title_list = df_title.loc[df_title.isOriginalTitle == 0, 'title'].to_list()
        alt_title_lang_list = df_title.loc[df_title.isOriginalTitle == 0, 'language'].to_list()

        imdb_id = title

        # Rip reviews:

        df_review_title = df_reviews_all.loc[df_reviews_all.imdb_id == title].copy()
        df_review_title = df_review_title.replace('\\N', '')

        review_text_list = df_review_title.text.to_list()
        review_score_list = df_review_title.score.to_list()

        # Rip roles:

        df_roles_principals = df_principals[df_principals.tconst == imdb_id].copy()
        df_roles_names = df_names[df_names.nconst_ind.isin(df_roles_principals.nconst_ind)].copy()

        df_roles = df_roles_principals.merge(df_names, how='left', on='nconst_ind')
        df_roles = df_roles.replace('\\N', '')

        roles_to_rip = [
            'actor',
            'self',
            'producer',
            'director',
            'writer',
            'cinematographer']

        # Make a dict from ripped data:
        role_dict = {}

        for role in roles_to_rip:
            role_dict[role] = df_roles.loc[df_roles.category == role].primaryName.to_list()

        insert_dict = { 'imdb_id': imdb_id, 
                        'orig_title': orig_title, 
                        'orig_title_lang': orig_title_lang, 
                        'alternate_titles': alt_title_list, 
                        'alternate_title_lang': alt_title_lang_list,
                        'review_texts': review_text_list,
                        'review_score_list': review_score_list,
                        'roles': role_dict
                        }

        mycol.insert_one(insert_dict)
