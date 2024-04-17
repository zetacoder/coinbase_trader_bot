
# Coinbase Trader Bot

Trading bot that connects to the Coinbase Advanced API to perform recurring purchases and sales of different assets everyday automatically.

## Stack
* Lenguage: Python
* Libraries: Coinbase Advanced API, math, crypto, uuid, dotenv
* Deployment: Render for Cron Jobs. https://render.com


### Strategy:

* Daily trading cryptocurrencies that have had an increase of %X of the price of the last 24hrs, taking advantage of the volatility of this type of assets.
* As soon as the asset has been bought at market price, the bot will create a sell order if the asset reaches a price = buy_price + target_profit_margin. For example, if I buy an apple at $10 and the profit we want is 5%, it will create a sell order, and our apple will be sold automatically when it reaches $15.
* Every day, every X hours it will check if there is balance in order to buy new products and create sales orders.

### Strategy Logic:
* I based the script on the logic that assets with high growth or short term uptrend cause more buying pressure, raising the price of the asset. This coupled with a conservative short term gain and choosing volatile assets allows to achieve small gains that accumulate over time.

### Strengths:
* By creating sell orders with a fixed profit percentage, it only sells assets when there is profit.
* Reinvests earnings, which can generate a powerful "compound interest" effect with relatively low initial investment.
* Low maintenance and effort costs. Once the script is created, it will run every day so I can use my time for other things.

### Weaknesses:
* Since it only sells once it reaches the profit margin, if this does not arrive soon it may take several days, or weeks before it returns to the price we want.
* If we enter in the trade in the top prices, we can suffer from massive sells in the market, dropping the prices to low to recover.



## Installation

1. Download and install python in your machine. https://www.python.org/downloads/

2. Move to the directory you want to install the trader bot. And clone the project

```bash
  cd path/to/your-project
  git clone https://github.com/zetacoder/coinbase_trader_bot.git
```
3. Install packages

```bash
  pip install -r requirements.txt
```
or 
```bash
  pip3 install -r requirements.txt
```
4. Set API enviroment

Create a .env file in the root directory with the API KEYS needed to connect your Coinbase API account. If you dont have one, register here: https://www.coinbase.com

```bash
API_KEY=""
API_SECRET="-----BEGIN EC PRIVATE KEY-----\YOUR-KEY-HERE\n-----END EC PRIVATE KEY-----\n"
USDC_WALLET_ID="THE WALLET ID YOU WANT TO USE (BTC, USDC, USD, EUR, ETC)"
```

5. Configure profit and product search:

Change the values in main.py to look for more or less volatile products and the profit you want to obtain selling the product.

```bash
MIN_PRICE_CHANGE_24_HRS = 6
TARGET_PERCENTAGE_PROFIT = .06
```

6. Run it!

```bash
python main.py
```

7. Deploy
If you want to deploy a cron job to run it everyday you can use:
* Render.com --> cron jobs
*  AWS Lambda with AWS Bridgeevents
*  Windows Scheduler tasks or crontab commands in MacOS/Linux

