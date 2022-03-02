from client import FtxClient

API_KEY = ""
API_SECRET = ""
SUBACCOUNT = ""
client = FtxClient(API_KEY, API_SECRET, SUBACCOUNT)


class Trade:

    def __init__(self, base_currency=None, quote_currency=None, amount=0, action=None, price=0, number_of_iceberg_order=1):
        self._base_currency = base_currency
        self._quote_currency = quote_currency
        self._amount = float(amount)
        self._action = action
        self._price = float(price)
        self._number_of_iceberg_order = int(number_of_iceberg_order)
        self.is_reverse = False
        self.market_name = ""
        self.find_market()

    def calculate_weight(self):
        '''
        Retrieve orderbook of market
        and calculate the average price
        '''
        orderbook = client.get_orderbook(self.market_name)

        if self._action == "buy":
            asks = orderbook['asks']
            weight = 0
            total = 0
            # if first ask fill the amount
            if asks[0][1] >= self._amount:
                return asks[0][0]
            for ask in asks:
                # if reversed currencies calculate price
                if self.is_reverse:
                    price = 1 / ask[0]
                    amount = ask[0] *ask[1]
                else:
                    price = ask[0]
                    amount = ask[1]
                total += amount
                # fill asks until reach total amount
                if total <= self._amount:
                    weight += price * amount
                else:
                    last_left_amount = self._amount - (total-amount)
                    weight += price * last_left_amount
                    average_price = weight / self._amount
                    return format(average_price,".8f")

        elif self._action == "sell":
            bids = orderbook['bids']
            weight = 0
            total = 0
            if bids[0][1] >= self._amount:
                return bids[0][0]
            for bid in bids:
                if self.is_reverse:
                    price = 1 / bid[0]
                    amount = bid[1] * bid[0]
                else:
                    price = bid[0]
                    amount = bid[1]
                total += amount
                print(total)
                if total <= self._amount:
                    weight += price * amount
                else:
                    last_left_amount = self._amount - (total - amount)
                    weight += price * last_left_amount
                    average_price = weight / self._amount
                    return average_price

    def find_market(self):
        '''
        check if market exists
        '''
        markets = client.list_markets()
        for market in markets:
            if market['baseCurrency'] == self._base_currency and market['quoteCurrency'] == self._quote_currency:
                self.market_name = market['name']
            # if the base and quote currency is switched
            elif market['baseCurrency'] == self._quote_currency and market['quoteCurrency'] == self._base_currency:
                self.is_reverse = True
                self.market_name = market['name']
                if self._action == "buy":
                    self._action = "sell"
                else:
                    self._action = "buy"

    def iceberg_order(self):
        '''
        Place iceberg order

        '''
        per_order_size = (self._amount * self._price) / self._number_of_iceberg_order
        response = []
        for order in range(self._number_of_iceberg_order):
            response.append({
                "Order_size": per_order_size,
                "Price": self._price,
                "Currency": self._quote_currency
            })
        return response



