import requests

from modules import db_connect as db


def find_country(country_name):
    id = False
    con, cur = db.connect()
    res = cur.execute("SELECT `id` FROM `country` WHERE `name` = %s", country_name)
    if res:
        row = cur.fetchone()
        id = row['id']
    con.close()
    return id


def insert_country(country):
    con, cur = db.connect()
    if find_country(country['name']['common']):
        return False
    cur.execute("INSERT INTO `country` (`name`, `cca2`) VALUES (%s, %s)",
                (country['name']['common'], country['cca2']))
    id = con.insert_id()
    con.commit()
    con.close()
    return id


data = requests.get('https://restcountries.com/v3.1/all').json()


for i in data:
    insert_country(i)
