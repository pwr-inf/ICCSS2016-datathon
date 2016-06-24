import traceback
import cPickle as pickle
from functools import partial
import multiprocessing
import os
from eventregistry import *

def get_page(page,path='',candidate=''):
    print page
    er=EventRegistry()
    er.login('kajdanowicz@gmail.com','qwpolkas')
    q = QueryEvents(keywords=[candidate],lang='eng')
    q.addRequestedResult(RequestEventsInfo(page = page, count = 200, sortBy = "size", sortByAsc = False))   
    res = er.execQuery(q)
    pickle.dump(res,open(path+candidate+'/'+str(page)+'.p','wb'))

def scrapp_candidate(candidate,path=''):
    try:
        print candidate
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path+candidate):
            os.makedirs(path+candidate)
        er=EventRegistry()
        er.login('kajdanowicz@gmail.com','qwpolkas')
        q = QueryEvents(keywords=[candidate],lang='eng')
        q.addRequestedResult(RequestEventsInfo(page = 1, count = 200, sortBy = "size", sortByAsc = False))   
        res = er.execQuery(q)
        pages=res['events']['pages']
        print 'pages for '+candidate+' '+str(pages)
        pickle.dump(res,open(path+candidate+'/1.p','wb'))
        pool=multiprocessing.Pool(48)
        map(partial(get_page,candidate=candidate,path=path),range(2,pages+1))
    except: 
        print 'ERROR FOR USER '+candidate
        traceback.print_exc()