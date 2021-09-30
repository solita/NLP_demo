import os
import pandas as pd

data_dir = '/home/ml_user/data/IMDb_raw'

# Read references to negative reviews for training data:

file_name = os.path.join(data_dir, 'aclImdb/train/urls_neg.txt')

df_train_neg_urls = pd.read_csv(file_name, sep='\s+', header=None)

print('Number of urls (train, neg): %d' % len(df_train_neg_urls))

file_list = []

for root, dirs, files in os.walk(os.path.join(data_dir, 'aclImdb/train/neg')):
    for file_name in files:
        if file_name.endswith('.txt'):
            file_list.append(file_name)

print('Number of urls (train, neg): %d' % len(file_list))
