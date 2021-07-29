import configparser

MONTH = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

config = configparser.RawConfigParser()
config.read("config.ini")

start_position = config.getint('Script', 'start_position')
restart_by_mins = config.getint('Script', 'restart')
date = config.getint('Script', 'date')
bot_token = config.get('Script', 'telegram_bot_token')
chat_id = config.get('Script', 'telegram_chat_id')


site = 'https://www.coingecko.com/en/coins/all'


def set_date(param):
    from datetime import datetime, timedelta, date

    if param == -1:
        return str(datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'))
    elif param == 0:
        return str(date.today())


find_date = set_date(date)
