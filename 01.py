import ccxt
import pprint
import pandas as pd

binance = ccxt.binance(config={
    'apiKey' : '',
    'secret' : '',
    'enableRateLimit' : True,
    'options' : {
        'defaultType' : 'future'
    }
})

# btc candle data taking
btc_ohlcv = binance.fetch_ohlcv(symbol="BTC/USDT", timeframe='1m', since=None, limit=627)   
# btc_OI = binance.fetchOpenInterestHistory(symbol="BTC/USDT", timeframe='3m', since=None, limit=86)
# print(btc_OI)

df = pd.DataFrame(data=btc_ohlcv, columns=["datetime","open","high","low","close","volume"])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)

start_price = 0
start_vol = 0
go_start_volume = 500 + 12800 + 3640
vol_skip_condition = 100000000000000000
oi_skipped_index = []

go_price = (btc_ohlcv[0][2]+btc_ohlcv[0][3])/2
go_volume = (((btc_ohlcv[0][4]-btc_ohlcv[0][1]) / (btc_ohlcv[0][2]-btc_ohlcv[0][3])) * btc_ohlcv[0][5]) + go_start_volume
# go_price = 0
# go_volume = 0
if start_price != 0:
    go_price = (start_price * abs(start_vol) + go_price * abs(go_volume)) / (abs(start_vol) + abs(go_volume))
    go_volume = start_vol + go_volume
go_price_start = go_price
go_volume_start = go_volume
print(go_price)

for index, i in enumerate(btc_ohlcv[1:]): 
    if i[5] >= vol_skip_condition:
        print("skipped", i[5])
        continue
    if index > 18300000:
        print (index, i)
        continue
    if go_volume >= 0:
        if i[4]-i[1] >= 0:
            if go_price >= (i[2]+i[3])/2:
                and_price = ((go_price * go_volume) + ((go_price + (i[2] - i[3])) * i[5]))
                and_volume = go_volume + i[5]
                # print("1")
                # print(and_volume)
                go_price = and_price / and_volume
                # print ("0")
            else:
                and_price = (go_price * go_volume) + (((i[2] + i[3]) /2 ) * i[5])
                and_volume = go_volume + i[5]
                # print("1")
                # print(and_volume)
                go_price = and_price / and_volume
        else:
            if go_volume <= ((abs(i[1]-i[4]) / (i[2]-i[3])) * i[5]):
               go_price = ((go_price * go_volume) + (((i[2]+i[3]) /2 ) * i[5])) / (go_volume + i[5])
            #    print("2")
            # else:
            #    print("3")
    else:
        if i[4]-i[1] < 0:
            if go_price <= (i[2]+i[3])/2:
                and_price = ((go_price * abs(go_volume)) + ((go_price - (i[2] - i[3])) * i[5]))
                and_volume = abs(go_volume) + i[5]
                # print("1")
                # print(and_volume)
                go_price = and_price / and_volume
                # print ("0")
            else:
                go_price = ((go_price * abs(go_volume)) + (((i[2]+i[3]) /2 ) * i[5])) / (abs(go_volume) + i[5])
                # print("4")
        else:
            if abs(go_volume) <= ((abs(i[1]-i[4]) / (i[2]-i[3])) * i[5]):
               go_price = ((go_price * abs(go_volume)) + (((i[2]+i[3]) /2 ) * i[5])) / (abs(go_volume) + i[5])
            #    print("5")
            # else:
            #    print("6")
    try:
        go_volume = go_volume + (((i[4]-i[1]) / (i[2]-i[3])) * i[5])
    except ZeroDivisionError:
        result = 0


print("start price : ", go_price_start)
print("start volume : ", go_volume_start)
print("current price :", go_price)
print("current extra volume :", go_volume)

# ch_p_4_birthday_gmil : H_1_! : GHY63KIDXQ6AYKQC : gmil_f2 : t3wm yxrp fdvu qx54 65bi pbwj 4exb foj5
# my_b(ameria_bread)_77_gmil : H_1_! : 35J4OTE7ZYHZYB5R : sxbm nbhh jnuk krup 7cku hxpg fdzn hlla
# 0x097B54505dD6C5c8054D8E10FA1aec8818D27Cf5   bird_move_right
# 0x09fE5ee1FC5644fC6d092b36c7cB1C20Ea7AC546   bro_bird_edge
# ast   rom dev7 hot   Butterfl
# jiro_katsuo   hea


# jokwo's skp      live:senior.webdeveloper2017
# Oobro's skp      live:.cid.693c580689439060
# liang's skp      live:.cid.888d9675171a4aca


# roman_dev7 : 6P4FINZW7EETUEE5
# roman_dev7 : E7U6I7HLB3QFC5WE
# roman_dev7 : 3IAMAQAIU2HHPYNL
# roman_dev trading_vew : U2TF 3443 DUVA ELJK
# roman_dev trading_vew backedup : rnEFctcd 20elpqWg WrzM3zSL jLYIMj2E uOuZVqIh 4KtIddx9
