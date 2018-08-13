import redis


r = redis.Redis(host='localhost',port=6379)

r.lpush('qqnews:start_urls','https://news.qq.com')
r.lpush('wangyinews:start_urls','https://news.163.com')
r.lpush('ifengnews:start_urls','https://news.ifeng.com')
r.lpush('sohunews:start_urls','https://news.sohu.com')
r.lpush('EastmoneyNews:start_urls','http://stock.eastmoney.com')
r.lpush('sinanews:start_urls','http://news.sina.com.cn/roll/#pageid=153')
r.lpush('peoplenews:start_urls','http://news.people.com.cn/')
r.lpush('toutiaonews:start_urls','https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A125AA5DDC88F50&cp=5ADC589F85308E1&_signature=uK7jowAA4n8SgaMj0J7VIbiu47')