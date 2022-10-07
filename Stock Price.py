import json
import requests
import time
import pandas as pd


def get_price(ticker):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    response = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance', headers=headers)
    response = json.loads(response.text)
    open_list = response['chart']['result'][0]['indicators']['quote'][0]['open']
    close_list = response['chart']['result'][0]['indicators']['quote'][0]['close']
    time_list = response['chart']['result'][0]['timestamp']
    df_list = []
    for i in range(len(time_list)):
        if close_list[i] is None or open_list[i] is None:
            continue
        price_diff = close_list[i] - open_list[i]
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_list[i]))
        result_dict = {'time': formatted_time, 'price difference': price_diff, 'close price': close_list[i], 'open price': open_list[i]}
        df_list.append(result_dict)
    df = pd.DataFrame(df_list)
    df.set_index('time', inplace=True)
    df.to_excel(f'{ticker}.xlsx')
    return df
get_price('GOOGLE')