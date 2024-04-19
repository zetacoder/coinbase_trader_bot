import os
import time
from dotenv import load_dotenv
from coinbase.rest import RESTClient
import uuid
import math


MIN_PRICE_CHANGE_24_HRS = 6
TARGET_PERCENTAGE_PROFIT = .06


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    # init api
    rest_client = RESTClient(api_key=api_key, api_secret=api_secret, verbose=False)

    # get account data
    wallet_id_usdc = str(os.getenv("USDC_WALLET_ID"))
    
   
    # open sell orders
    active_orders = rest_client.list_orders(order_side="SELL", order_status=["OPEN"])
    
    products_being_selled = []
    for order in active_orders['orders']:
        products_being_selled.append(order['product_id'])
    
    
    # get spot products to buy filtering by price change in 24hrs
    to_buy = []
    spot_products = rest_client.get_products(product_type="SPOT")
    for spot_product in spot_products["products"]:
        price_change = spot_product['price_percentage_change_24h']
        product_id = str(spot_product['product_id'])
        if product_id.endswith('USDC') and float(price_change) > MIN_PRICE_CHANGE_24_HRS and not product_id in products_being_selled:
            to_buy.append(spot_product)
    
    total_balance = float(rest_client.get_account(wallet_id_usdc)['account']['available_balance']['value'])
    valid_amount = False
    number_of_products_to_buy = len(to_buy)
    to_spend_on_each_product = (total_balance / number_of_products_to_buy) * .98
    
    while not valid_amount:
        if to_spend_on_each_product > 1:
            valid_amount = True
        else:
            number_of_products_to_buy -= 1
            to_spend_on_each_product =  (total_balance / number_of_products_to_buy)
    
    
    for product in to_buy[:number_of_products_to_buy]:
        usdc_balance = float(rest_client.get_account(wallet_id_usdc)['account']['available_balance']['value'])
        
        # get data of the product
        product_id = product['product_id']
        price = float(product['price'])
        quote_increment = float(product['quote_increment'])
        quote_min_size= float(product['quote_min_size'])
        order_id = str(uuid.uuid4())
        quote_size = round((to_spend_on_each_product +  quote_increment), 2)
        
        if quote_size > usdc_balance:
            print(f'Skipping product: {product_id}. Current quote size: {quote_size}, current balance: {usdc_balance}')
            continue
        
        rest_client.market_order_buy(client_order_id=order_id, product_id=product_id, quote_size=str(quote_size))
        time.sleep(5)
        sell_limit_product(rest_client=rest_client, product_id=product_id, buy_price=price)
        time.sleep(2)
        
    
    
def sell_limit_product(rest_client: RESTClient, product_id: str, buy_price: float):
    client_order_id = str(uuid.uuid4())
    base_currency = product_id.split("-")[0]
    
    # get product pair data
    product = rest_client.get_product(product_id=product_id)
    
    min_base_size = product['base_min_size']
    
    # get product wallet account
    wallets = rest_client.get_accounts()
    for wallet in wallets['accounts']:
        if wallet['currency'] == base_currency:
            product_wallet = wallet
    

    quantity_of_asset = round(float(product_wallet['available_balance']['value']), 4)
   
    limit_price = round(buy_price * (1 + TARGET_PERCENTAGE_PROFIT), 4)
    
    if float(quantity_of_asset) < float(min_base_size):
        print(f"You dont have sufficient asset to sell. Current: {quantity_of_asset} | Min to sell: {min_base_size}")
        return
    
    rest_client.limit_order_gtc_sell(client_order_id=client_order_id, product_id=product_id, base_size=str(quantity_of_asset), limit_price=str(limit_price))
    
    

if __name__ == "__main__":
    main()


