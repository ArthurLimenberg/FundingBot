def buy(exchange, data):

    for symbol in data[1]:
        symbol_formats = dict()
        symbol_formats['mainSymbol'] = symbol.split(':')[1]
        symbol_formats['pair'] = symbol.split('/')[0] + symbol_formats['mainSymbol']

        balance = exchange.fetch_balance()
        free_currency = balance['free'][symbol_formats['mainSymbol']]
        print(f"Баланс: {free_currency} {symbol_formats['mainSymbol']}")
        if free_currency >= 10.0:
            index_for_order = 0
            markets = exchange.load_markets()
            for symbol, market_data in markets.items():
                print(market_data)
            order_book = exchange.fetch_order_book(symbol, limit=10)
            while free_currency > 10 or data[0][symbol]['Approximate volume']:
                order_book = exchange.fetch_order_book(symbol, limit=10)

            first_order = order_book['bids'][index_for_order] \
                if data[0][symbol]['fundingRate'] > 0 else order_book['asks'][index_for_order]
            print(f'first order : {first_order} not usdt')

            start_price = first_order[0]
            price = start_price
            volume_in_main_currency = start_price * first_order[1] / 2

            print(f'{symbol}: {start_price} - main currency \n volume in main currency: {volume_in_main_currency} \n common valume: {data[0][symbol]["Approximate volume"]} - main \n free {free_currency}')

            while amount_contracts < (data[0][symbol]['Approximate volume'] if free_currency > data[0][symbol]['Approximate volume'] else free_currency / first_order[0]):

                quantity = round(first_order[1] / 2, 3) if volume_in_main_currency < data[0][symbol]['Approximate volume'] \
                    else ((round(data[0][symbol]['Approximate volume'] / price, 3) if
                        free_currency > data[0][symbol]['Approximate volume'] else free_currency / price))

                print(quantity, end='\n---')
                break

                order_params = {
                    'symbol': symbol,
                    'side': 'sell',
                    'type': 'LIMIT',
                    'price': price,
                    'amount': quantity,
                    'params': {
                        'isIsolated': True,
                        'leverage': 1,
                    }
                }

                #open_order = exchange.create_order(**order_params)
                #order_id = open_order['info']['orderId']
                #order_info = exchange.fetch_order(order_id, symbol=symbol)
                #pprint(order_info)
                #if order_info['status'] == 'open':
                #    break

        else:
            print(symbol + ': ' + Fore.RED + 'Not enough currency' + Fore.RESET)


def sell():
    pass
