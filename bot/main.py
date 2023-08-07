import colorama
from colorama import Fore
from pprint import pprint
from _services._funding_service import find_best_funding
from _config._exchange import binance
from _services._trading_service import buy

colorama.init()

if __name__ == '__main__':

    print(Fore.LIGHTYELLOW_EX + '\nSearching funding:')
    best_funding = find_best_funding(binance)
    pprint(best_funding)
    info = buy(binance, best_funding)
    pprint(info)


