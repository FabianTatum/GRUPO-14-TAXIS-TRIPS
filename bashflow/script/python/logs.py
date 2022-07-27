from datetime import datetime as dt

def log(message):
    print(f'[{str(dt.now())[:19]}] - {message}')
