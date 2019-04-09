import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
coinArray = []

currencyFile = open("currency.txt", "r")
chosen_currency = str(currencyFile.read().strip())

start = datetime.now()

def get_coin_price(coin):
	COIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/' + coin + '/?convert=' + chosen_currency.upper()
	response = requests.get(COIN_API_URL)
	response_json = response.json()
	rsp = response_json[0]
	class coin:
		name = rsp['name']
		price = rsp['price_' + chosen_currency]
		change24 = rsp['percent_change_24h']
		symbol = rsp['symbol']
		old_price = float(price) * (1-float(change24)/100) #old price of coin
		gain24 = float(price) - float(old_price) #24 hour dollar gain
	coinArray.append(coin)

coins = []
coinFile = open("coins.txt", "r")
for line in coinFile:
	coins.append(str(line).strip())

coinFile.close()

amount_coins = []
amountFile = open("amount_coins.txt", "r")
for line in amountFile:
	amount_coins.append(float(line.strip()))

amountFile.close()

####################################################LOOP#################################
while True:
	for coin in coins:
		get_coin_price(coin)
	coinArray.sort(key=lambda coin: coin.name)

	new_money = 0
	old_money = 0
	money_gain24 = 0
	

	for item in coinArray:
		item.name = item.name.replace(' ', '-')
		item.currentAmount = amount_coins[coins.index(str(item.name).lower())]
		item.currentValue = float(item.currentAmount)*float(item.price)
		item.oldValue = float(item.currentAmount)*float(item.old_price)
		old_money += float(item.oldValue) #yesterdays worth
		new_money += float(item.currentValue) #todays worth

		totalchange24 = (new_money - old_money)/old_money * 100 #percentage
		money_gain24 = new_money - old_money #fiat
		#print item.name + " " + str(item.gain24)
		#print(item.name + "(" + item.symbol + "): \n" + "Price: " + str(round(float(item.price),2)) + " NOK\n" + "Change 24h: " + item.change24 + "%\n" + "Current Amount: " + str(item.currentAmount) + " " + item.symbol + "\n" + "Current Value: " + str(item.currentValue) + " NOK\n")

	#print (str(round(money_gain24, 2)) + " NOK\n")
	#print (str(round(totalchange24, 2)) + "%\n")
	#print (str(old_money) + "\n" + str(new_money))

	prefix = ""
	if totalchange24 > 0:
		prefix = "+"
	else:
		prefix = "" 
	f = open("index.html", "w")
	html_value = ("""<!DOCTYPE html>
	<html lang="en">
	<head>
	  <meta charset="UTF-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	  <meta http-equiv="X-UA-Compatible" content="ie=edge">
	  <link rel='stylesheet' type='text/css' href='main.css'>
	  <title>Worthlet</title>
	  <meta http-equiv="refresh" content="60">
		<link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
	</head>
	<body>
	  <div id='big-text' class='cont'>	
	  <h1>""" + prefix + """<span id='percent_change'>""" + str(round(totalchange24,2)) + """</span><span class='smalltext'>%<span></h1>
	  <h2>""" + prefix + str(round(money_gain24, 2)) + """<span class='smalltext'>""" + chosen_currency.upper() + """</span></h2>
	  <h3>""" + str(round(new_money,2)) + """<span class='smalltext'>""" + chosen_currency.upper() + """</span></h3>
	  </div>
	  <div id='currencies' class='cont'>
	  </div>

	</body>
	<script type='text/javascript'>
	let h1var = document.querySelector('#percent_change').innerHTML;
	h1var = Number(h1var)
	  if(h1var > 0) {
	    document.querySelector('body').style.backgroundColor = '#4CBB17';
	  }
	  else {
	    document.querySelector('body').style.backgroundColor = '#8b0000';
	  }
	</script>
	</html>
	 """)
	
	
	soup = BeautifulSoup(html_value, "html.parser")
	original_tag = soup.find(id="currencies")

	for coin in coinArray:
		new_div = soup.new_tag('div')
		if float(coin.change24)>0:
			new_div['class'] = "currency"
		else:
			new_div['class'] = "currency negative"
		new_name = soup.new_tag('p')
		new_name.string = coin.name
		new_div.append(new_name)
		new_price = soup.new_tag('p')
		new_price.string = str(round(float(coin.price),2)) + " " + chosen_currency.upper()
		new_div.append(new_price)
		new_change = soup.new_tag('p')
		new_change.string = str(coin.change24) + "%"
		new_div.append(new_change)
		new_currentAmount = soup.new_tag('p')
		new_currentAmount = soup.new_tag('p')
		new_currentAmount.string = str(round(coin.currentAmount,8)) + " " + coin.symbol
		new_div.append(new_currentAmount)
		new_currentValue = soup.new_tag('p')
		new_currentValue.string = str(round(coin.currentValue,2)) + " " + chosen_currency.upper()
		new_div.append(new_currentValue)
		original_tag.append(new_div)

	new_time = soup.new_tag('p')
	new_time['class'] = "time-keeper"
	new_time.string = "©Erik Skår, 2019 | Last updated: " + str(datetime.now())[:-7]
	body_tag = soup.body
	body_tag.append(new_time)
	f.write(str(soup))
	f.close()

	coinArray = []
	print("running successfully " + str(datetime.now())[:-7])
	now = str(datetime.now() - start)[:-7]
	print("uptime: " + now)

	time.sleep(60)