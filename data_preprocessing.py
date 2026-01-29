## smart platform testing
## lib
import os
import pandas as pd

### data preprocessing

def get_csv_files(folder_path):
    csv_files=[]
    for files in os.listdir(folder_path):
        if files.endswith('.csv'):
            csv_files.append(os.path.join(folder_path,files))
    return csv_files

csv_files= get_csv_files('../amazon-products-dataset/versions/2')


# store the data in dat frame
dataframes= []
for path in csv_files:
    df = pd.read_csv(path)
    dataframes.append(df)
    
combined_df= pd.concat(dataframes,ignore_index=True)

### basic info
combined_df.head()

combined_df.head()

combined_df = combined_df.drop(combined_df.columns[-1], axis=1)
combined_df.drop(['name','image','link'],axis=1,inplace=True)

combined_df.shape

combined_df=combined_df.dropna()

combined_df.info()

combined_df.columns = (combined_df.columns.str.strip().str.lower().str.replace(" ","_"))

combined_df= combined_df[
    pd.to_numeric(combined_df['ratings'],errors= 'coerce').between(0,5)
]
combined_df['ratings'] = combined_df['ratings'].astype(float)

combined_df['no_of_ratings']= (
    combined_df['no_of_ratings'].astype(str)
    .str.replace(',','')
    .where(lambda x:x.str.fullmatch(r'\d+'))
    .astype(float)
)

price_pattern = r'^₹\d{1,3}(,\d{3})*$'
cols = ['discount_price','actual_price']

masked = (
    combined_df[cols]
    .astype(str)
    .apply(lambda x:x.str.match(price_pattern))
    .all(axis=1)
)

combined_df = combined_df[masked]

combined_df[cols] = (
    combined_df[cols]
    .replace({'₹':'',',':''},regex=True)
    .astype(float)
)

combined_df.info()

combined_df['main_category'].unique()