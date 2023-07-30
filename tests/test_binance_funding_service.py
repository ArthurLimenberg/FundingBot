import mock
from unittest import TestCase
from bot._services._funding_service import find_best_funding

class TestBinanceFundingService(TestCase):
    
    def test_should_find_best_funding(self):
        # Given
        exchange_mock = mock.Mock()
        exchange_mock.fetchFundingRates.return_value = {
            'USDT:ETH': {'fundingRate': 1.5, 'symbol': 'USDT:ETH', 'fundingTimestamp': 122},
            'USDT:BTC': {'fundingRate': 2.5, 'symbol': 'USDT:BTC', 'fundingTimestamp': 123}
        }
        exchange_mock.fetch_order_book.return_value = {
            'asks': [
                [9.0, 557.4],
                [9.598, 631.5],
                [9.599, 1144.3],
                [9.615, 2121.8],
                [9.95, 276.3],
                [10.0, 579.7],
                [10.09, 495.5],
                [10.9, 105.1]
            ],
            'bids': [
                [8.701, 4663.0],
                [8.7, 3211.2],
                [8.696, 431.1],
                [8.679, 57.4],
                [8.6, 11.6],
                [8.5, 637.9],
                [8.32, 360.5],
                [8.3, 72.2],
                [8.26, 72.3],
                [8.174, 574.3]
            ],
            'datetime': '2023-07-29T08:13:35.413Z',
            'nonce': 33132944216,
            'symbol': 'INJ/USDT:USDT',
            'timestamp': 1690618415413
        }

        # When
        result = find_best_funding(exchange_mock)

        # Then TODO add asserts
        print(f'results : {result}')