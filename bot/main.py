import colorama
from colorama import Fore
from _services._funding_service import find_best_funding, output_info, buy
from _config._exchange import binance

colorama.init()

if __name__ == '__main__':


    print(Fore.RESET + '\nSearching funding:')
    best_funding = find_best_funding(binance)

    if best_funding:
        output_info(best_funding)
        buy(binance, best_funding)