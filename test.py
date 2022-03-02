import requests
url = 'http://127.0.0.1:8000/quote'
url2 = 'http://127.0.0.1:8000/quote_iceberg'
myobj = {'action': 'buy',
         'base_currency': 'USD',
         'quote_currency': 'BTC',
         'amount': '10000.0'}

myobj2 = {'action': 'sell',
         'base_currency': 'BTC',
         'quote_currency': 'USD',
         'amount': '100.0',
          "price": 21,
          "number_of_iceberg_order": 2}

x = requests.post(url2, json=myobj2)
print(x.text)
