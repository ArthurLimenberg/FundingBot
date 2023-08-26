import colorama
from colorama import Fore
from pprint import pprint
from _services._funding_service import find_best_funding
from _config._exchange import binance
from _services._trading_service import entering


colorama.init()

if __name__ == '__main__':

    print(Fore.LIGHTYELLOW_EX + '\nSearching funding:')
    best_funding = find_best_funding(binance)
    if best_funding:
        pprint(best_funding)
        entering(best_funding)
        server_time = binance.fetch_time()
        while server_time < best_funding[0].timestamp:
            pprint(server_time)
            server_time = binance.fetch_time()
        else:
            balance = binance.fetch_balance()

            for symbol in balance['info']['positions']:
                amount = float(symbol['positionAmt'])
                if amount != 0:

                    order = binance.create_market_order(
                        symbol=symbol['symbol'],
                        side='sell' if amount > 0 else 'buy',
                        amount=abs(amount)
                    )
    else:
        print('Sorry. Funding not found')


