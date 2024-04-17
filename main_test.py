from coinbase.rest import RESTClient

def sell_asset(rest_client:  RESTClient, client_order_id: str, product_id: str, base_size: float, limit_price: float):
    sell_response = rest_client.limit_order_gtc_sell(client_order_id=client_order_id, product_id=product_id,base_size=str(base_size),limit_price=str(limit_price))
    