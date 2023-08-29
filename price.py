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


country_name = input().strip().lower()
country_code = find_country_code(country_name)


game_name = input().strip().lower()
app_ids = find_appid(game_name)

if not app_ids:
    print('Игра не найдена')
else:
    pass


# url = f'https://store.steampowered.com/api/appdetails?appids={appid}&cc={country_code}&filters=price_overview'
