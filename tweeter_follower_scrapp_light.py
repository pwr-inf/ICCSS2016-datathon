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
user_template=Template('https://mobile.twitter.com/$user')
followers_template=Template('https://mobile.twitter.com/$user/followers')
followers_template_cursor=Template('https://mobile.twitter.com/$user/followers?cursor=$cursor')


def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default

def get_all_followers(user,path):
    print 'Getting all followers for '+user
    if not os.path.exists(path):
        os.makedirs(path)
    headers={}
    uri_to_go=followers_template.substitute({'user':user})
    index=0
    hasNextPage=True
    while(hasNextPage):
        print 'current page:'+uri_to_go
        retry=0
        page=requests.get(uri_to_go,headers=headers)
        while page.status_code!=200:
            if retry%10==0:
                print 'Too many requests!'
            retry+=1
            time.sleep(1)
            page=requests.get(uri_to_go,headers=headers)
        page_soup = BeautifulSoup(page.content, 'html.parser')
        user_names=set()
        names=map(lambda x:x.split("/")[1].split('?')[0],
                filter(lambda x:x.find('?p=s')!=-1,
                       map(lambda x:x.attrs['href'],page_soup.find_all('a',href=True))))
        user_names.update(names) 
        with open(path+user+'_'+str(index)+'.p', 'wb') as fp:
            pickle.dump(user_names, fp)
        index+=1
        try:
            uri_to_go=filter(lambda x:x.find('cursor=')!=-1,
                             map(lambda x:x.attrs['href'],
                                 page_soup.find_all('a',href=True))
                            )[0]
            uri_to_go=followers_template_cursor.substitute({'user':user,'cursor':uri_to_go.split('=')[1]})
            print 'next page:'+uri_to_go
        except :
            traceback.print_exc()
            hasNextPage=False