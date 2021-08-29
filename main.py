# ライブラリのインポート
import requests
import configparser
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

def job():
    ini = configparser.ConfigParser()
    ini.read('./config.ini', 'UTF-8')

    # 設定のロード
    API_URL_POINT = str(ini['JPMAP']['API_URL_POINT'])
    API_URL_AREA = str(ini['JPMAP']['API_URL_AREA'])
    API_URL_AREA_CODE = str(ini['JPMAP']['API_URL_AREA_CODE'])
    API_TYPE = str(ini['SETTING']['API_TYPE'])
    PRODUCT = str(ini['SETTING']['PRODUCT'])
    INTERVAL = str(ini['SETTING']['INTERVAL'])
    START_DATE = str(ini['SETTING']['START_DATE'])
    END_DATE = str(ini['SETTING']['END_DATE'])
    SAVE_FILE_NAME = str(ini['SETTING']['SAVE_FILE_NAME'])
    POINT_LAT = str(ini['POINT']['POINT_LAT'])
    POINT_LON = str(ini['POINT']['POINT_LON'])
    AREA_NLAT = str(ini['AREA']['AREA_NLAT'])
    AREA_WLON = str(ini['AREA']['AREA_WLON'])
    AREA_SLAT = str(ini['AREA']['AREA_SLAT'])
    AREA_ELON = str(ini['AREA']['AREA_ELON'])
    AREA_CODE_1 = str(ini['AREA_CODE']['AREA_CODE_1'])
    AREA_CODE_2 = str(ini['AREA_CODE']['AREA_CODE_2'])


    if API_TYPE == "0":
        # APIに接続するための情報（「?」の後ろに「&」で条件を繋いでいく）
        API_Endpoint = API_URL_POINT \
                        + "?product=" + PRODUCT \
                        + "&lat=" + POINT_LAT \
                        + "&lon=" + POINT_LON \
                        + "&interval="+ INTERVAL \
                        + "&start=" + START_DATE \
                        + "&end=" + END_DATE
    elif API_TYPE == "1":
        API_Endpoint = API_URL_AREA \
                        + "?product=" + PRODUCT \
                        + "&interval="+ INTERVAL \
                        + "&nlat=" + AREA_NLAT \
                        + "&wlon=" + AREA_WLON \
                        + "&slat=" + AREA_SLAT \
                        + "&elon=" + AREA_ELON \
                        + "&start=" + START_DATE \
                        + "&end=" + END_DATE
    elif API_TYPE == "2":
        API_Endpoint = API_URL_AREA_CODE \
                        + "?product=" + PRODUCT \
                        + "&regioncode=" + AREA_CODE_1 + "_" + AREA_CODE_2 \
                        + "&interval="+ INTERVAL \
                        + "&start=" + START_DATE \
                        + "&end=" + END_DATE
    print(API_Endpoint)

    # API接続の実行
    response = requests.get(API_Endpoint).json()
    # pprint.pprint(response['data'])
    # pprint.pprint(response['data'])

    response_df = pd.DataFrame(response['data'])
    response_df['date'] = pd.to_datetime(response_df['date'], format='%Y-%m-%d')
    response_df['value'] = response_df['value'].astype(np.float64)
    response_df = response_df.set_index('date')
    response_df = response_df[(np.abs(stats.zscore(response_df)) < 3).all(axis=1)]

    print(response_df)

    save_file_name = "data"
    response_df.to_csv("./downloads/" + save_file_name + ".csv")

    response_df.plot()
    plt.title(save_file_name)
    plt.savefig("./downloads/" + save_file_name + ".png", bbox_inches='tight')
    plt.close('all')


if __name__ == '__main__':
    job()