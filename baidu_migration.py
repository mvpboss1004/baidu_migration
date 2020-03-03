#coding: utf-8
import requests
import pandas as pd
import json
from datetime import date, timedelta
from progressbar import progressbar

def baidu_migration_rank(target_region, result_region, id, move_type, move_date):
    url = f'''https://huiyan.baidu.com/migration/{result_region}rank.jsonp?dt={target_region}&id={id}&type=move_{move_type}&date={move_date.strftime('%Y%m%d')}'''
    df = pd.DataFrame(json.loads(requests.get(url).text[3:-1])['data']['list'])
    df['value'] /= 100
    return df

with pd.ExcelWriter(f'migration_to_sz_{date.today()}.xlsx') as writer:
    dt = date.today()
    df = []
    for i in progressbar(range(40)):
        dt -= timedelta(days=1)
        try:
            dfi = baidu_migration_rank('city', 'province', '440300', 'in', dt)
            dfi = dict(zip(dfi.province_name, dfi.value))
            dfi['move_date'] = dt
            df.append(dfi)
        except Exception as e:
            print(e)
    df = pd.DataFrame(df)
    df.to_excel(writer, sheet_name='province', index=False)

    dt = date.today()
    df = pd.DataFrame(columns=['city_name', 'province_name', 'value', 'move_date'])
    for i in progressbar(range(40)):
        dt -= timedelta(days=1)
        dfi = baidu_migration_rank('city', 'city', '440300', 'in', dt)
        dfi['move_date'] = dt
        df = pd.concat([df,dfi], ignore_index=True)
    df.to_excel(writer, sheet_name='city', index=False)
