import os
import pandas as pd

data_dir = '/home/ml_user/data/IMDb_raw'

# Read references to negative reviews for training data:

file_name = os.path.join(data_dir, 'aclImdb/train/urls_neg.txt')

df_train_neg_urls = pd.read_csv(file_name, sep='\s+', header=None)

df_train_neg_urls.head()
