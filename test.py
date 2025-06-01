import pandas as pd
import requests

def get_inr_to_idr_rate():
    url = 'https://open.er-api.com/v6/latest/INR'
    response = requests.get(url)
    data = response.json()
    return data['rates']['IDR']

conversion_rate = get_inr_to_idr_rate()

def convert_inr_to_idr(inr_price):
    inr_price = float(inr_price.replace(',', ''))
    idr_price = inr_price * conversion_rate
    return idr_price

def format_price(price):
    return price - (price % 1000000)

data_raw = pd.read_csv('complete laptop data0.csv', encoding = 'unicode_escape')

wanted_columns=['name','Model Name','Processor Brand','Processor Name','Processor Generation','SSD Capacity','RAM','Operating System','Screen Size','Price','link']
df_ori = data_raw[wanted_columns]

df = df_ori.copy()

df['brand'] = df['name'].apply(lambda x: x.split()[0] if x else '')

df['processor'] = df['Processor Brand'] + ' ' + df['Processor Name']+ ' ' + df['Processor Generation']
df = df.drop(['Processor Brand','Processor Name','Processor Generation'],axis=1)

df = df.rename(columns={'SSD Capacity':'ssd','Model Name':'series','RAM':'ram','Operating System':'os','Screen Size':'display','Price':'price'})
df = df[['brand','series','processor','os','ssd','ram','display','price','name','link']]

df['display'] = df['display'].str.extract(r'\(([\d\.]+) inch\)', expand=False)

df = df.map(lambda x: x.replace('?', '') if isinstance(x, str) else x)
df['price'] = df['price'].apply(convert_inr_to_idr)
df['price'] = df['price'].astype(str)
df['price'] = df['price'].apply(lambda x: f"{int(x.split('.')[0]):}")

df = df.fillna(' ')

df['brand'] = df['brand'].str.lower()
df['series'] = df['series'].str.lower()
df['processor'] = df['processor'].str.lower()
# df['gpu'] = df['gpu'].str.lower()
df['os'] = df['os'].str.lower()
df['ssd'] = df['ssd'].str.lower()
df['ram'] = df['ram'].str.lower()
df['display'] = df['display'].str.lower()
df['price'] = df['price'].str.lower()
df = df.drop(['name'],axis=1)
df['link'] = df['link'].str.lower()
df = df.drop_duplicates(keep='first')

df.reset_index(drop=True, inplace=True)
df['index'] = df.index

df['price'] = df['price'].astype(int)
df['pricing'] = df['price'].apply(format_price)

df = df.sort_values(by=['index'], ascending=True)
df = df[['index'] + [col for col in df.columns if col != 'index']]

df.to_csv('clean_data.csv', index=False, encoding='utf-8-sig')

df.drop(['price', 'link'], axis=1, inplace=True)

lst = []
indices = [] 
for k in range(df.shape[0]):
    n = [str(df.iloc[k, i]) for i in [1,3,4,5,6,7,8]]
    n = ' '.join(n)  # Gabungkan nilai menjadi satu string
    lst.append(n)
    indices.append(df.iloc[k,0])  # Menyimpan indeks baris

def remove_duplicate_words(text):
    seen = set()
    result = []
    for word in text.split():
        if word.lower() not in seen:
            seen.add(word.lower())
            result.append(word)
    return ' '.join(result)


dataset_spec = pd.DataFrame({'index': indices, 'specification': lst})
dataset_spec['specification'] = dataset_spec['specification'].apply(remove_duplicate_words)

dataset_spec.to_csv('dataset_spec.csv', index=False, encoding='utf-8-sig')