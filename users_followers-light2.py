import tweeter_follower_scrapp_light as tfs
import traceback
import multiprocessing;

users=['BarackObama','HillaryClinton','GovRichardson','BernieSanders','MartinOMalley','LincolnChafee','JimWebbUSA','JohnKasich','tedcruz','marcorubio','JebBush','NJGovChristie','CarlyFiorina','RickSantorum']

def get_followers(user):
    try:
        tfs.get_all_followers(user,'tweeter_followers-light2/'+user+'/')
    except:
        print 'ERROR FOR USER ' + user
        traceback.print_exc()

pool=multiprocessing.Pool(24)


        
pool.map(get_followers,users)
