# Worthlet
## -How much is my wallet worth?

A simple Python back-end paired with a HTML/CSS/JS front-end to easily track how much your crypto wallet is currently worth and how much it has changed the past 24 hours.

Perfect for that raspberry pi you have laying around the house that you don't know what to do with!
### Features
- Track:
    - Total wallet worth in the FIAT currency of your choice
    - Total wallet percentage and FIAT worth change the last 24 hours
    - Name, price, 24h percentage change, current amount and FIAT worth of each individual coin
    - All prices are fetched every 60 seconds directly from coinmarketcap!
- Changing background color for your total gain / loss
    - Green for when you have earned money the last 24 hours and red for when you've lost money
- Individual background color change for each of your coins
    - Same as above, but for each individual coin
    - The coin that has the highest percentage increase the past 24 hours will be highlighted in blue
- Easy addition and removal of your coins
    - Add and remove lines from 2 .txt files to make sure you only track the coins you want
### Instructions
1. Add the name of your coins in the **coins.txt** file.
2. Put the amount of each coin in the **amount_coins.txt** file.
    - Remember to only put one amount on each line, and to match up the line numbers with your respective coins.
3. (Optional) If you want you can change the FIAT currency in the **currency.txt** file. 
4. Then you just run **script.py** (preferably in Python 3) and open **index.html** in the browser of your choice. Remember to fullscreen! :)
    - When changing your coins / amounts / currency, remember to restart **script.py**, because at the moment live update of those are disabled to reduce the workload on updates.

### Troubleshooting
If you for some reason need to install BeautifulSoup (shouldn't be needed), then just run:
```pip install bs4```

### Planned features / changes
- Better scaling for smaller screens and many currencies
- Something more exciting in the background than just colors
- Some general code cleanup to make it a little more understandable if someone wants to make their own version
- Direct wallet integration would be nice, but there aren't many wallets that support a lot of coins which have public APIs :(

### Donations
If you for some reason like this enough to consider donating to me:
- ETH: ```0xe7dfBA3c4c4E0AED216F04ae3CE4Fa08Fed6E53F```
- BTC: ```1mWeeTra1emnFDgVT16JevUYXBkKJ9qVJ ```
- NANO:  ```xrb_1om6bxywwsgzibbhseyuqwed4f717cemj866d45qqwjh4sbgbxind6niusdx```
