from fastapi import FastAPI, HTTPException, Response
from database import BitcoinPriceDatabase
import requests
import time

app = FastAPI()
bitcoinDatabase = BitcoinPriceDatabase().instance()


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/bitcoin/{currency}")
def get_bitcoin_price(currency, response: Response):
    try:
        price_data = bitcoinDatabase.get_bitcoin_price(currency)

        if(price_data is not None):
            current_time = time.time()

            if (current_time - price_data["timestamp"] > 300):
                price_data = get_coinlib_price(currency)
                
                if(price_data is None):
                    response.status_code = 500
                    return {"detail": "Error when trying to get price"}

                bitcoinDatabase.insert_bitcoin_price(price_data)

        if(price_data is None):
            price_data = get_coinlib_price(currency)
            
            if(price_data is None):
                response.status_code = 500
                return {"detail": "Error when trying to get price"}

            bitcoinDatabase.insert_bitcoin_price(price_data)

        return price_data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")



def get_coinlib_price(currency):
    api_key = "Your_api_key_here"
    request = requests.get(
        f"https://coinlib.io/api/v1/coin?key={api_key}&pref={currency}&symbol=BTC")
    if(request.status_code == 200):
        coinlib = request.json()
        print(coinlib)

        price_data = {
            "currency": currency,
            "price": round(float(coinlib["price"].replace(',', '.')), 2),
            "delta_1h": round(float(coinlib["delta_1h"].replace(',', '.')), 2),
            "delta_24h": round(float(coinlib["delta_24h"].replace(',', '.')), 2),
            "delta_7d": round(float(coinlib["delta_7d"].replace(',', '.')), 2),
            "delta_30d": round(float(coinlib["delta_30d"].replace(',', '.')), 2),
        }
        
        print(price_data)

        return price_data
    
    return None
