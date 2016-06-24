import tweeter_follower_scrapp as tfs
import traceback
users=['realDonaldTrump','BarackObama','HillaryClinton','GovRichardson','BernieSanders','MartinOMalley','LincolnChafee','JimWebbUSA','JohnKasich','tedcruz','marcorubio','JebBush','NJGovChristie','CarlyFiorina','RickSantorum']


for user in users:
    try:
        tfs.get_all_followers(user,'tweeter_followers/'+user+'/')
    except:
        print 'ERROR FOR USER ' + user
        traceback.print_exc()