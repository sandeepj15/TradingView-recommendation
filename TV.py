import json
import urllib.request as request
import requests
import pandas as  pd
from tradingview_ta import TA_Handler, Interval, Exchange


with request.urlopen('https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true') as response:
    source = response.read()
    data = json.loads(source)


usd_pair = []
for i in  range(len(data['data'])):
    coin_usd = {}
    if data['data'][i]['q'] == "USDT":
        coin_usd['coin'] = data['data'][i]['s']
        coin_usd['price'] = data['data'][i]['c']
        usd_pair.append(coin_usd)
        

rec = []


for i in range(len(usd_pair)):
    pair ={}
    output = TA_Handler(
        symbol= usd_pair[i]['coin'],
        screener="crypto",
        exchange="binance",
        interval=Interval.INTERVAL_4_HOURS,
    )
    
    
    pair['Coin'] = usd_pair[i]['coin']
    pair['RECOMMENDATION']=  output.get_analysis().summary['RECOMMENDATION']
    pair['price']= usd_pair[i]['price']
    rec.append(pair)


              
strong_rec = []

for i in range(len(rec)):
    rec_coin ={}
    if rec[i]['RECOMMENDATION'][:6:] == 'STRONG':
        rec_coin['Coin']= rec[i]['Coin'] 
        rec_coin['Recommendation'] = rec[i]['RECOMMENDATION']  
        rec_coin['Price in USDT'] = rec[i]['price']
        strong_rec.append(rec_coin)
        

dff = pd.DataFrame(strong_rec)
dff
