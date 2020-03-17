import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

print('---------------------------------------------')
print('Loading .env ....')
print('Using VIRTUAL_ENV = ', os.getenv('VIRTUAL_ENV'))
print('Successfully loaded .env')
print('---------------------------------------------')
