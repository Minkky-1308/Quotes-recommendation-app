import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    DATA_PATH = 'data/quotes.csv'