import requests
import configparser
import pymysql


def db_connect():
    config = configparser.ConfigParser()
    config.read('config.ini')
    con = pymysql.connect(host = config.get('db_local', 'host'),
                            user=config.get('db_local', 'user'),
                            password=config.get('db_local', 'password'),
                            db=config.get('db_local', 'db'),
                            cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    return con, cur


def find_appid(appid):
    id = False
    con, cur = db_connect()
    res = cur.execute("SELECT `id` FROM `games` WHERE `appid` = %s", appid)
    if res:
        row = cur.fetchone()
        id = row['id']
    con.close()
    return id


def insert_appid(game):
    con, cur = db_connect()
    if find_appid(game['appid']):
        return False
    cur.execute("INSERT INTO `games` (`appid`, `name`) VALUES (%s, %s)",
                (game['appid'], game['name']))
    id = con.insert_id()
    con.commit()
    con.close()
    return id


data = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/').json()['applist']['apps']['app']


for i in data:
    if i['name'] != '':
        insert_appid(i)
