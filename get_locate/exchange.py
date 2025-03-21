import pandas as pd
import geocoder
from geopy.geocoders import Nominatim
from folium import Map, Marker, IFrame, Popup, Icon
import requests
import xml.etree.ElementTree as ET
import time
import urllib
import yaml

with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)
towns = data.get('towns', [])  

for town in towns:
    # CSVファイルの読み込み
    df = pd.read_csv(f'./addresses/address_{town}.csv')

    # 緯度と経度の列を初期化
    geolocator = Nominatim(user_agent="user-id")
    df['latitude'] = None
    df['longitude'] = None

    # 緯度と経度のジオコーディングまたは既存の値の使用
    base_url = "https://www.geocoding.jp/api/"

    for index, row in df.iterrows():
        address = '愛媛県' + row['address']

        if address:
            while True:  # 再試行のための無限ループ
                try:
                    # APIリクエストを送信
                    params = {'q': address}
                    response = requests.get(base_url, params=params)
                    time.sleep(10)

                    # レスポンスの内容をXMLとして解析
                    if response.status_code == 200:
                        xml_content = response.content
                        root = ET.fromstring(xml_content)

                        # 緯度と経度を取得
                        df.loc[index, 'latitude'] = float(root.find(".//lat").text)
                        df.loc[index, 'longitude'] = float(root.find(".//lng").text)
                        print(f'index: {index}')
                        break  # 成功した場合、ループを抜ける
                    else:
                        print(f"住所 '{address}' のジオコーディングに失敗しました。再試行まで3600秒待ちます。")
                        time.sleep(3600)
                except Exception as e:
                    print(f"住所 '{address}' のジオコーディング中にエラーが発生しました: {e}")
                    time.sleep(3600)  # エラーの場合も待機後に再試行
        else:
            print(f"行 {index} の住所情報が不足しています。")

    df.to_csv(f'./coordinates/coordinates_{town}.csv')