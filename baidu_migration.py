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

def historycurve(target_region, id, move_type):
    url = '''http://huiyan.baidu.com/migration/historycurve.jsonp?dt={target_region}&id={id}&type=move_{move_type}'''
    return json.loads(requests.get(url).text[3:-1])['data']['list']

def historycurve_all(target_region, move_type):
    curves = []
    if target_region == 'province':
        province = pd.read_csv('province_id.csv')
        for i in progressbar(range(len(province))):
            row = province.iloc[i]
            try:
                df = pd.DataFrame(historycurve(target_region,row.province_id,move_type).items(), columns=['date_key','historycurve']).sort_values(bye='date_key')
            except Exception as e:
                print(row)
                pring(e)
            else:
                df['province'] = row.province_name
                curves.append(df)
    elif target_region == 'city':
        province_city = pd.read_csv('province_city_id.csv')
        for i in progressbar(range(len(province_city))):
            row = province_city.iloc[i]
            try:
                df = pd.DataFrame(historycurve(row.city_id,row.city_id,move_type).items(), columns=['date_key','historycurve']).sort_values(by='date_key')
            except Exception as e:
                print(row)
                print(e)
            else:
                df['province'] = row.province_name
                df['city'] = row.city_name
                curves.append(df)
    return pd.concat(curves, ignore_index=True)

def internalflowhistory(id, move_date):
    url = f'''http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt=city&id={id}&date={move_date.strftime('%Y%m%d')}'''
    return json.loads(requests.get(url).text[3:-1])['data']['list']

def internalflowhistory_all():
    move_date = date.today()
    province_city = pd.read_csv('province_city_id.csv')
    curves = []
    for i in progressbar(range(len(province_city))):
        row = province_city.iloc[i]
        try:
            df = pd.DataFrame(internalflowhistory(row.city_id, move_date).items(), columns=['date_key','internal_flow']).sort_values(by='date_key')
        except Exception as e:
            print(row)
            print(e)
        else:
            df['province'] = row.province_name
            df['city'] = row.city_name
            curves.append(df)
    return pd.concat(curves, ignore_index=True)