from pathlib import Path
from dotenv import dotenv_values

script_path = Path(__file__).resolve().parent
env_file_path = script_path.parent.parent / '.env'
__env_file = dotenv_values(env_file_path)


variables = {
    'API_KEY': __env_file['API_KEY'],
    'SECRET_KEY': __env_file['SECRET_KEY'],
    'IS_TEST': True if (__env_file['IS_TEST'] == 'true') else False,
    'MINIMUM_FUNDING_PERCENTAGE': float(__env_file['MINIMUM_FUNDING_PERCENTAGE']),
    'PRICE_DEVIATION_PERCENTAGE': float(__env_file['PRICE_DEVIATION_PERCENTAGE'])
}