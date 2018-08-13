import json
import pymysql
import redis


def saveitem(r,conn,item):
    if r.llen(item) > 0:
        source, data = r.blpop(item,timeout=1)
        item = json.loads(data.decode('utf-8'))
        try:
            with conn.cursor() as cur:
                cur.execute( r'''
                insert into mynews (title,pubtime,url,tag,refer,body) 
                VALUES ('%s','%s','%s','%s','%s','%s')'''%(item['title'],item['pubtime'],item['url'],item['tag'],item['refer'],item['body']))
                conn.commit()
                print("[%s] inserted %s" % (item['refer'],item['title']))
        except Exception as e:
            pass
    else:
        pass



conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='news',charset='utf8')

r = redis.Redis(host='localhost',port=6379)


def run():
    while True:
        saveitem(r, conn, 'qqnews:items')
        saveitem(r, conn, 'ifengnews:items')
        saveitem(r, conn, 'sohunews:items')
        saveitem(r, conn, 'wangyinews:items')
        saveitem(r, conn, 'EastmoneyNews:items')
        saveitem(r, conn, 'sinanews:items')
        saveitem(r, conn, 'peoplenews:items')
        saveitem(r, conn, 'toutiaonews:items')


