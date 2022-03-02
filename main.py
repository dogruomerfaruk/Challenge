from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from trade import Trade
app = FastAPI()


class Market(BaseModel):
    action: str
    base_currency: str
    quote_currency: str
    amount: float


class Limit(BaseModel):
    action: str
    base_currency: str
    quote_currency: str
    amount: float
    price: float
    number_of_iceberg_order: Optional[int] = 1


@app.post("/quote")
def market_order(data: Market):

    trade = Trade(data.base_currency, data.quote_currency, data.amount, data.action)
    if trade.market_name == "":
        raise HTTPException(status_code=404, detail="Market Not Found")
    else:
        price = trade.calculate_weight()
        total = price * float(data.amount)
        return {"total": str(total),
                "price": "{:.8f}".format(price),
                "currency": data.quote_currency}


@app.post("/quote_iceberg")
def limit_order(data: Limit):
    print(data)
    trade = Trade(data.base_currency, data.quote_currency, data.amount, data.action, data.price, data.number_of_iceberg_order)
    if trade.market_name == "":
        raise HTTPException(status_code=404, detail="Market Not Found")
    else:
        return trade.iceberg_order()


def check_parameters(data):
    if "number_of_iceberg_order" in dict(data).keys():
        if data.number_of_iceberg_order > 5 or data.number_of_iceberg_order < 1:
            raise HTTPException(status_code=404, detail="number_of_iceberg_order must be 1 to 5")

    if data.price <= 0:
        raise HTTPException(status_code=404, detail="price must be positive")

    if data.amount <= 0:
        raise HTTPException(status_code=404, detail="amount must be positive")

    if data.price < 0:
        raise HTTPException(status_code=404, detail="price must be positive")




