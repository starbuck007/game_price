import configparser
import pymysql


def connect():
    config = configparser.ConfigParser()
    config.read('config.ini')
    con = pymysql.connect(host = config.get('db_local', 'host'),
                            user=config.get('db_local', 'user'),
                            password=config.get('db_local', 'password'),
                            db=config.get('db_local', 'db'),
                            cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    return con, cur
