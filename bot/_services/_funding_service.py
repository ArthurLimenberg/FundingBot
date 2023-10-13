import ccxt
from pprint import pprint
from pystreamapi import Stream
from collections import namedtuple
from bot._config._env import variables as env

Funding = namedtuple('Funding', ['symbol', 'rate', 'timestamp'])
FundingWithOrderBook = namedtuple('FundingWithOrderBook', ['symbol', 'rate', 'timestamp', 'order_book'])
FundingWithVolume = namedtuple('FundingWithVolume', ['symbol', 'rate', 'timestamp', 'volume'])

minimum_funding_percentage = env['MINIMUM_FUNDING_PERCENTAGE']
price_deviation_percentage = env['PRICE_DEVIATION_PERCENTAGE']


def is_funding_rate_valid(funding_rate: float, minimum_funding_percentage: float) -> bool:
    return ((minimum_funding_percentage * -1) > funding_rate >= -0.01) \
        or (0.01 >= funding_rate > minimum_funding_percentage)


def fetch_order_book(platform, funding: Funding) -> FundingWithOrderBook:
    try:
        order_book = platform.fetch_order_book(symbol=funding.symbol, limit=10)
    except ccxt.ExchangeError:
        order_book = []
        print(f'>>> Can\'t fetch order book for: {funding.symbol}')

    return FundingWithOrderBook(funding.symbol, funding.rate, funding.timestamp, order_book)


def calculate_approximate_volume(funding: FundingWithOrderBook, price_deviation_percentage: float) -> FundingWithVolume:
    CupPair = namedtuple('CupPair', ['price', 'volume'])

    order_book = funding.order_book
    cup_asks = order_book['asks']
    cup_bids = order_book['bids']
    if cup_asks and cup_bids:
        best_cup_ask = order_book['asks'][0][0]
        best_cup_bid = order_book['bids'][0][0]

        sum_asks = Stream.of(cup_asks) \
            .filter(lambda pair: pair[0] <= best_cup_ask + (best_cup_ask * price_deviation_percentage)) \
            .map(lambda pair: pair[0] * pair[1]) \
            .reduce(lambda a, b: a + b) \
            .or_else_get(0)

        sum_bids = Stream.of(cup_bids) \
            .filter(lambda pair: pair[0] <= best_cup_bid + (best_cup_bid * price_deviation_percentage)) \
            .map(lambda pair: pair[0] * pair[1]) \
            .reduce(lambda a, b: a + b) \
            .or_else_get(0)

        volume = sum_bids + sum_asks

        while volume >= 10000:
            volume /= 5
    else:
        volume = 0

    return FundingWithVolume(funding.symbol, funding.rate, funding.timestamp, round(volume, 3))


def find_best_funding(exchange: ccxt.Exchange) -> list[FundingWithVolume]:

    """Searching best funding pairs"""

    try:
        funding_rates = exchange.fetchFundingRates()
    except ccxt.NetworkError as e:
        print(exchange.id, 'failed to fetch funding rates due to a network error:', str(e))
    except ccxt.ExchangeError as e:
        print(exchange.id, 'failed to fetch funding rates due to exchange error:', str(e))
    except Exception as e:
        print(exchange.id, 'failed to fetch funding rates with:', str(e))
    else:
        return Stream.of(funding_rates.items()) \
            .map(lambda item: Funding(symbol=item[0], rate=item[1]['fundingRate'], timestamp=item[1]['fundingTimestamp'])) \
            .filter(lambda funding: is_funding_rate_valid(funding.rate, minimum_funding_percentage)) \
            .map(lambda funding: fetch_order_book(exchange, funding)) \
            .filter(lambda funding: funding.order_book) \
            .map(lambda funding: calculate_approximate_volume(funding, price_deviation_percentage)) \
            .filter(lambda funding: funding.volume) \
            .sorted(lambda a, b: -(abs(a.rate) - abs(b.rate))) \
            .to_list()


