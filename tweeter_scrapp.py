import requests
import time
from bs4 import BeautifulSoup
import sys
import time
from string import *
import requests.packages.urllib3
import multiprocessing
import cPickle as pickle
import traceback
from functools import partial
import os

requests.packages.urllib3.disable_warnings()

max_retry=10000

# proxies = {'http': "socks5://gold.engine.kdm.wcss.pl:9050"}
# proxies['https']=proxies['http']

def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default
    
def get_stat(stats,index):
    stat=safe_list_get(map(lambda x:x.get_text(),stats),index,'')
    stat=stat.replace('K','000')
    stat=stat.replace(',','')
    stat=stat.replace('.','')
    return stat
def get_tweet_details(tweet_id,user='',retry=0):
    print tweet_id
    try:
        headers_custom= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        text_selector=".TweetDetail-text.u-textLarge"
        stat_selector='.TweetDetail-statCount, .TweetAction-count'
        tweet_template=Template('https://mobile.twitter.com/$user/status/$tweet_id')
        uri=tweet_template.substitute({'user':user,'tweet_id':tweet_id})
        response=requests.get(uri,headers=headers_custom)
        if response.status_code != 200:
            if retry%10==0:
                print 'Too many requests in tweet download!'
            time.sleep(1)
            return get_tweet_details(tweet_id,user=user,retry=retry+1) if retry<max_retry else {}
        soup = BeautifulSoup(response.content, 'html.parser')
        text=safe_list_get(map(lambda x:x.get_text(),soup.select(text_selector)),0,'')
        stats=soup.select(stat_selector)
        pases=get_stat(stats,0)
        likes=get_stat(stats,1)
        date=soup.select('.TweetDetail-timeAndGeo')
        date=map(lambda d:d.get_text(),date)
        responses=soup.select('.Timeline-base .Tweet-body')
        def response_to_data(r):
                user_name=r.select('.UserNames-screenName')[0].get_text()
                text=r.select('.Tweet-text')[0].get_text()
                date=r.select('.Tweet-timestamp time')[0].attrs['datetime']
                return {'text':text,'user':user_name,'date':date}
        responses=map(response_to_data,responses)
        return {'text':text,'pases':pases,'likes':likes,'date':safe_list_get(date,0,''),'responses':responses}
    except :
        traceback.print_exc()
        return {}

def get_all_tweets(user,path):
    print 'Getting all tweets for '+user
    if not os.path.exists(path):
        os.makedirs(path)
    user_template=Template('https://mobile.twitter.com/$user')
    twitter_template=Template('https://mobile.twitter.com$rest_url')
    headers={}
    pool=multiprocessing.Pool()
    uri_to_go=user_template.substitute({'user':user})
    index=0
    hasNextPage=True
    while(hasNextPage):
        print 'current page:'+uri_to_go
        page=requests.get(uri_to_go,headers=headers)
        retry=0
        while page.status_code!=200:
            if retry%10==0:
                print 'Too many requests in page download!'
            retry+=1
            time.sleep(1)
            page=requests.get(uri_to_go,headers=headers)
        page_soup = BeautifulSoup(page.content, 'html.parser')
        tweet_ids=set()
        ids=map(lambda x:x.split("/")[3].split('?')[0],
                filter(lambda x:x.find('/status/')!=-1,
                       map(lambda x:x.attrs['href'],page_soup.find_all('a',href=True))))
        tweet_ids.update(ids) 
        new_tweets_data=pool.map(partial(get_tweet_details,user=user),tweet_ids)
        with open(path+user+'_'+str(index)+'.p', 'wb') as fp:
            pickle.dump(new_tweets_data, fp)
        index+=1
        try:
            uri_to_go=filter(lambda x:x.find('max_id=')!=-1,
                             map(lambda x:x.attrs['href'],
                                 page_soup.find_all('a',href=True)))[0]
            uri_to_go=twitter_template.substitute({'rest_url':uri_to_go})
            print 'next page:'+uri_to_go
        except :
            traceback.print_exc()
            hasNextPage=False