import requests
import re


from modules import db_connect as db


def find_country_code(name):
    code = False
    con, cur = db.connect()
    res = cur.execute("SELECT `cca2` FROM `country` WHERE `name` = lower(%s)", name)
    if res:
        row = cur.fetchone()
        code = row['cca2']
    con.close()
    return code


def find_appid(name):
    escaped_game = escape_special_characters(name)
    appid = False
    con, cur = db.connect()
    res = cur.execute(f"SELECT `appid` FROM `game` WHERE `name` like lower('%{escaped_game}%')")
    con.close()
    if res:
        appid = cur.fetchall()
    return appid


def escape_special_characters(string):
    special_characters = r".^$*+?{}[]\|'()"
    escaped_string = re.sub(r'([' + re.escape(special_characters) + r'])', r'\\\1', string)
    return escaped_string


country_name = input('Введите название страны: ').strip().lower()
country_code = find_country_code(country_name)


game_name = input('Введите название игры: ').strip().lower()
app_ids = find_appid(game_name)

request_appid_list = []
if app_ids:
    for app_id in app_ids:
        request_appid_list.append(app_id['appid'])
else:
        print('Игра не найдена')
        exit()


request_appid = ','.join(request_appid_list)


url = f'https://store.steampowered.com/api/appdetails?appids={request_appid}&cc={country_code}&filters=price_overview'


prices = requests.get(url).json()
print(prices)


for price in prices:
    if prices[price]['success']:
        if prices[price]['data']['price_overview']['discount_percent'] > 0:
            print(price, 'Цена со скидкой:', prices[price]['data']['price_overview']['final_formatted'], 'Скидка:', prices[price]['data']['price_overview']['discount_percent'], 'Цена:', prices[price]['data']['price_overview']['initial_formatted'])
        else:
            print(price, prices[price]['data']['price_overview']['final_formatted'])
    else:
        print(price, prices[price])
