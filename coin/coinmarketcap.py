# -*- coding: utf-8-*-
# @Date    : 2018-02-08
# @Author  : yuhaifeng
# @Website :
# @Description1:  获取coinmarketcap数据
# @Tools-Required:

import requests
import json


class CoinData():
    coin = {}
    dataUrl = 'https://api.coinmarketcap.com/v1/ticker/?limit=0&convert=CNY'

    def __init__(self):
        data = requests.get(self.dataUrl).json()
        # 初始化字典
        for item in data:
            self.coin[item['symbol']] = item['id']

    # market_cap_cny 市值
    # price_cny 单价
    # total_supply 流通总量
    # 24h_volume_cny 24小时流通总量
    # percent_change_1h 最近1小时
    def getCoinInfo(self, symbol):
        coin_id = self.coin[symbol]
        url = f'https://api.coinmarketcap.com/v1/ticker/{coin_id}/?convert=CNY'
        info = requests.get(url).json()
        return info
        if info:
            for i in info:
                data = {
                    'name': i['name'],
                    'price_cny': i['price_cny'],
                    'market_cap_cny': i['market_cap_cny'],
                    'total_supply': i['total_supply'],
                    '24h_volume_cny': i['24h_volume_cny'],
                    'percent_change_1h': i['percent_change_1h']
                }



if __name__ == "__main__":
    coin = CoinData()
    for i in coin.getCoinInfo('BTC'):
        print(i)
