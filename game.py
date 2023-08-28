import requests

from modules import db_connect as db


def find_appid(appid):
    id = False
    con, cur = db.connect()
    res = cur.execute("SELECT `id` FROM `game` WHERE `appid` = %s", appid)
    if res:
        row = cur.fetchone()
        id = row['id']
    con.close()
    return id


def insert_appid(game):
    con, cur = db.connect()
    if find_appid(game['appid']):
        return False
    cur.execute("INSERT INTO `game` (`appid`, `name`) VALUES (%s, %s)",
                (game['appid'], game['name']))
    id = con.insert_id()
    con.commit()
    con.close()
    return id


data = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/').json()['applist']['apps']['app']


for i in data:
    if i['name'] != '':
        insert_appid(i)
