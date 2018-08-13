from celery import Celery
from celery.schedules import crontab
from scrapy import cmdline
from redis import Redis
import pymysql
from .saveinmysql import run


# 生成Celery对象,设置broker存储地址为redis://localhost:6379/1
app = Celery('tasks', broker='redis://localhost:6379/1')

r = Redis(host='127.0.0.1', port=6379)
r1 = Redis(host='127.0.0.1', port=6379, db=1)
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='news', charset='utf8')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Master爬虫启动
    # 让Master的程序每隔一段时间执行一次,这里设置为5s
    sender.add_periodic_task(60, push_url.s())
    # sender.add_periodic_task(30, saveitem.s())
    sender.add_periodic_task(600, truncate_redis.s())

    sender.add_periodic_task(60, run_EastmoneyNews.s())
    sender.add_periodic_task(60, run_qqnews.s())
    sender.add_periodic_task(60, run_wangyinews.s())
    sender.add_periodic_task(60, run_ifengnews.s())
    sender.add_periodic_task(60, run_sohunews.s())
    sender.add_periodic_task(60, run_sinanews.s())
    sender.add_periodic_task(60, run_peoplenews.s())
    sender.add_preeriodic_task(60, run_toutiaonews.s())

    # 设置为在某个时间点执行,以下为每周一到周五早上9点25分集合竞价结束时运行收集数据,时区相差8小时
    sender.add_periodic_task(crontab(hour='10', minute='55',day_of_week='1,2,3,4,5'), save.s())

@app.task
def truncate_redis():
    r1.flushdb()



@app.task
def push_url():
    r.lpush('qqnews:start_urls', 'https://news.qq.com')
    r.lpush('wangyinews:start_urls', 'https://news.163.com')
    r.lpush('ifengnews:start_urls', 'https://news.ifeng.com')
    r.lpush('sohunews:start_urls', 'https://news.sohu.com')
    r.lpush('EastmoneyNews:start_urls', 'http://stock.eastmoney.com')
    r.lpush('sinanews:start_urls', 'http://news.sina.com.cn/roll/#pageid=153')
    r.lpush('peoplenews:start_urls', 'http://news.people.com.cn/')
    r.lpush('toutiaonews:start_urls','https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A125AA5DDC88F50&cp=5ADC589F85308E1&_signature=uK7jowAA4n8SgaMj0J7VIbiu47')

@app.task
def run_EastmoneyNews():
    cmdline.execute("scrapy crawl EastmoneyNews".split())

@app.task
def run_peoplenews():
    cmdline.execute("scrapy crawl peoplenews".split())

@app.task
def run_sinanews():
    cmdline.execute("scrapy crawl sinanews".split())

@app.task
def run_qqnews():
    cmdline.execute("scrapy crawl qqnews".split())


@app.task
def run_ifengnews():
    cmdline.execute("scrapy crawl ifengnews".split())

@app.task
def run_sohunews():
    cmdline.execute("scrapy crawl sohunews".split())

@app.task
def run_wangyinews():
    cmdline.execute("scrapy crawl wangyinews".split())

@app.task
def run_toutiaonews():
    cmdline.execute("scrapy crawl toutiaonews".split())

@app.task
def save():
    run()