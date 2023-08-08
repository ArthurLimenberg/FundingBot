import ccxt
from ._env import variables


binance = ccxt.binanceusdm({
    'apiKey': variables['API_KEY'],
    'secret': variables['SECRET_KEY'],
    'options': {
        'defaultType': 'future',
        'defaultContractType': 'PERPETUAL',
        'test': variables['IS_TEST'],
    }
})
binance.set_sandbox_mode(variables['IS_TEST'])

