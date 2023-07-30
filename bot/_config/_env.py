from dotenv import dotenv_values

__env_file = dotenv_values(".env")

variables = {
    'API_KEY': __env_file['API_KEY'],
    'SECRET_KEY': __env_file['SECRET_KEY'],
    'IS_TEST': True if (__env_file['IS_TEST'] == 'true') else False,
    'MINIMUN_FUNDING_PERCENTAGE': float(__env_file['MINIMUN_FUNDING_PERCENTAGE']),
    'PRICE_DEVIATION_PERCENTAGE': float(__env_file['PRICE_DEVIATION_PERCENTAGE'])
}