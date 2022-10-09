import json
import requests
import time
import pandas as pd
import numpy as np
from scipy.stats import kurtosis



def get_price(ticker, cumulative=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    response = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance', headers=headers)
    response = json.loads(response.text)
    open_list = response['chart']['result'][0]['indicators']['quote'][0]['open']
    close_list = response['chart']['result'][0]['indicators']['quote'][0]['close']
    time_list = response['chart']['result'][0]['timestamp']
    df_list = []
    current_date = 'unknown'
    cumulative_price_diff = 0
    for i in range(len(time_list)-1):
        if close_list[i] is None or open_list[i] is None:
            continue
        price_diff = close_list[i] - open_list[i]
        price_av = (close_list[i] + open_list[i])/2
        cumulative_price_diff = cumulative_price_diff + price_diff
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_list[i]))
        current_date = time.strftime('%Y-%m-%d', time.localtime(time_list[i]))
        result_dict = {'time': formatted_time, 'price difference': price_diff, 'close price': close_list[i], 'open price': open_list[i], 'mid price': price_av, 'cumulative price difference' : cumulative_price_diff}
        df_list.append(result_dict)
    df = pd.DataFrame(df_list)
    df.set_index('time', inplace=True)
    df.to_csv(f'stock_price_data/{ticker} {current_date}.csv')
    return mathematical_calculations(df)


def mathematical_calculations(price_df):
    price_df.set_index('price difference', inplace=True)
    print(price_df)
    price_diff_array = price_df.index.to_numpy().astype(float)
    print(price_diff_array)
    print(np.mean(price_diff_array))
    print(np.sort(price_diff_array))
    print(np.std(price_diff_array))
    print(np.percentile(price_diff_array, 97.5))
    print(kurtosis(price_diff_array))
    mean = np.mean(price_diff_array)
    std = np.std(price_diff_array)
    kurt = kurtosis(price_diff_array)

def implied_norm(x,mean, std):
    return (1/(std*(np.sqrt(2*(np.pi))))*np.exp(-((x-mean)**2)/(2*(std)**2)))


print(implied_norm(0.1,1,0.1))
get_price('AAPL')
get_price('META')
get_price('GOOGL')