import requests
import time
coinArray = []

def get_coin_price(coin):
	COIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/' + coin + '/?convert=NOK'
	response = requests.get(COIN_API_URL)
	response_json = response.json()
	rsp = response_json[0]
	class coin:
		name = rsp['name']
		price = rsp['price_nok']
		change24 = rsp['percent_change_24h']
		symbol = rsp['symbol']
		old_price = float(price) * (1-float(change24)/100) #old price of coin
		gain24 = float(price) - float(old_price) #24 hour dollar gain
	coinArray.append(coin)

coins = ['bitcoin', 'ethereum', 'stellar', 'decred', 'salt', 'dash', 'litecoin', 'icon', 'omisego']
amount_coins = [0.00426363, 0.526026623632742, 64.925, 0.2391478, 1.5285804, 0.222474, 0.194639, 12.42636, 0.9669056]
while True:
	for coin in coins:
		get_coin_price(coin)
	coinArray.sort(key=lambda coin: coin.change24, reverse=True)

	new_money = 0
	old_money = 0
	money_gain24 = 0
	

	for item in coinArray:
		item.currentAmount = amount_coins[coins.index(str(item.name).lower())]
		item.currentValue = float(item.currentAmount)*float(item.price)
		item.oldValue = float(item.currentAmount)*float(item.old_price)
		old_money += float(item.oldValue) #yesterdays worth
		new_money += float(item.currentValue) #todays worth
		totalchange24 = (new_money - old_money)/old_money * 100 #percentage
		money_gain24 = new_money - old_money #fiat
		#print item.name + " " + str(item.gain24)
		print(item.name + "(" + item.symbol + "): \n" + "Price: " + str(round(float(item.price),2)) + " NOK\n" + "Change 24h: " + item.change24 + "%\n" + "Current Amount: " + str(item.currentAmount) + " " + item.symbol + "\n" + "Current Value: " + str(item.currentValue) + " NOK\n")

	print str(round(totalchange24, 2)) + "%\n"
	print str(round(money_gain24, 2)) + " NOK\n"
	print str(old_money) + "\n" + str(new_money)
	prefix = ""
	if totalchange24 > 0:
		prefix = "+"
	else:
		prefix = "" 
	f = open("index.html", "w")
	f.write("""<!DOCTYPE html>
	<html lang="en">
	<head>
	  <meta charset="UTF-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	  <meta http-equiv="X-UA-Compatible" content="ie=edge">
	  <link rel='stylesheet' type='text/css' href='main.css'>
	  <title>Ticker</title>
	  <meta http-equiv="refresh" content="60">
	</head>
	<body>
	  <h1>""" + prefix + """<span id='percent_change'>""" + str(round(totalchange24,2)) + """</span><span class='smalltext'>%<span></h1>
	  <h2>""" + prefix + str(round(money_gain24, 2)) + """<span class='smalltext'>NOK</span></h2>
	  <p>Total:</p>
	  <h3>""" + str(round(new_money,2)) + """<span class='smalltext'>NOK</span></h3>

	</body>
	<script type='text/javascript'>
	let h1var = document.querySelector('#percent_change').innerHTML;
	h1var = Number(h1var)
	  if(h1var > 0) {
	    document.querySelector('body').style.backgroundColor = 'green';
	  }
	  else {
	    document.querySelector('body').style.backgroundColor = 'red';
	  }
	</script>
	</html>
	 """)
	f.close()
	coinArray = []
	time.sleep(60)