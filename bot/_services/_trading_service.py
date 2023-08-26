from pystreamapi import Stream
from collections import namedtuple
from bot._config._exchange import binance
from pprint import pprint


def get_first_price(symbol: str, side: str) -> tuple:
    return binance.fetch_order_book(symbol=symbol, limit=5)['bids' if side == 'sell' else 'asks'][0]


def separate_symbols(symbol: str) -> dict:
    separated_symbols = symbol.replace('/', '').split(':')
    separated_symbols_dict = dict()
    separated_symbols_dict['pair'], separated_symbols_dict['main'] = separated_symbols
    return separated_symbols_dict


def search_main_currency_balance(symbol: str, data: dict) -> float:
    return data['free'][symbol]


def search_pair(symbol: str, data: dict) -> float:
    return float([position['positionAmt'] for position in data['info']['positions'] if position['symbol'] == symbol][0])


def get_balance(symbol: str) -> tuple:
    return (search_main_currency_balance(separate_symbols(symbol)['main'], binance.fetch_balance()),
            search_pair(separate_symbols(symbol)['pair'], binance.fetch_balance()))


def precision_amount(pair: str) -> float:
    return binance.load_markets()[pair]['precision']['amount']


def fetch_min_amount(pair: str):
    for market in binance.fetch_markets():
        if market['symbol'] == pair:
            return market['limits']['cost']['min']


def entering(data: list):
    suc_data = []
    for pair in data:
        balance = get_balance(pair.symbol)
        print(balance)
        if balance[0]:
            side = 'sell' if pair.rate > 0 else 'buy'
            print(side)
            print(f'balans_{pair.symbol} = {balance[0]}\n pair = {balance[1]}')
            binance.set_leverage(1, symbol=pair.symbol)
            while balance[0] > fetch_min_amount(pair.symbol) or balance[1] < pair.volume:
                price, amount = get_first_price(pair.symbol, side)
                amount = amount / 2 if balance[0] >= (amount / 2) * price else balance[0] / price
                if fetch_min_amount(pair.symbol) <= amount * price:
                    print(f'кол-во {amount}\n price = {price}')
                    order = binance.create_limit_order(
                        symbol=separate_symbols(pair.symbol)['pair'],
                        side=side,
                        amount=amount,
                        price=price,
                        params={'leverage': 1}
                    )
                    pprint(order)
                    order_status = binance.fetchOrder(id=order['id'], symbol=pair.symbol)['status']
                    while order_status != 'closed':
                        order_status = binance.fetchOrder(id=order['id'], symbol=pair.symbol)['status']
                        print(order_status)
                    else:
                        print("sucsessful")
                        balance = get_balance(pair.symbol)

                else:
                    break
            else:
                suc_data.append(pair)
        else:
            print('no money')

    return suc_data


def exiting():
    pass
