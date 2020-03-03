#coding: utf-8
import requests
import pandas as pd
import json
from datetime import date, timedelta
from progressbar import progressbar
import os

def rank(target_region, result_region, id, move_type, move_date):
    url = f'''https://huiyan.baidu.com/migration/{result_region}rank.jsonp?dt={target_region}&id={id}&type=move_{move_type}&date={move_date.strftime('%Y%m%d')}'''
    df = pd.DataFrame(json.loads(requests.get(url).text[3:-1])['data']['list'])
    df['value'] /= 100
    return df

def internalflowhistory(id, move_date):
    url = f'''http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt=city&id={id}&date={move_date.strftime('%Y%m%d')}'''
    return json.loads(requests.get(url).text[3:-1])['data']['list']

def internalflowhistory_all():
    move_date = date.today()
    province_city = pd.read_csv('province_city_id.csv')
    curves = []
    for idx,row in progressbar(pd.read_csv('province_city_id.csv').iterrows()):
        curve = pd.DataFrame(internalflowhistory(row.city_id, move_date), columns=['date_key','internal_flow'])
        curve['province'] = row.province_name
        curve['city_name'] = row.city_name
        curves.append(curve)
    return pd.concat(curves, ignore_index=True)