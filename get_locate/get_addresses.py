import pandas as pd
import yaml

with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)
towns = data.get('towns', [])  

# towns = ['西田乙', '西田甲', '西田新開', '西田西新開', '西泉乙', '西泉丁', '西泉甲', '西泉西新開', '西泉東新開', '楢木', '坂元乙', '坂元甲', '野々市', '北山', '禎瑞']
# towns = ['楢木']
# towns = ['西田乙', '西田甲', '西田新開', '西田西新開', '西泉乙', '西泉丁', '西泉甲', '西泉西新開', '西泉東新開', '楢木', '坂元乙', '坂元甲', '野々市', '北山']

# mt_parcel_city382060.csvを読み込み、prc_idを文字列として扱う
df_parcel = pd.read_csv('./source_data/38206-5003-search-list.csv', encoding='cp932')
valid_condition = df_parcel['地番'].str.match(r'^[甲乙丙丁0-9\-]+$', na=False)
df_parcel.loc[valid_condition, 'address'] = df_parcel['地番区域'] + df_parcel['地番']

# oaza_cho列が指定された文字列のいずれかに一致する行を抽出
for town in towns:
    pattern = town
    # pattern = '|'.join(towns)
    df_parcel_filtered = df_parcel[df_parcel['address'].str.contains(pattern, na=False)]

    df_parcel_filtered.to_csv(f'./addresses/address_{town}.csv')