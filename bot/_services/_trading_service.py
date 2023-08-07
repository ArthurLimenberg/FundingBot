from pystreamapi import Stream
from collections import namedtuple
from bot._config._env import variables as env
from ccxt import binanceusdm


def buy(exchange: binanceusdm, data: namedtuple):
    symbol = data
    return exchange.createLimitBuyOrder()


def sell():
    pass
