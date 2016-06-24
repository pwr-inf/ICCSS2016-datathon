import tweeter_scrapp as ts
import traceback
oldUsers=set(['realDonaldTrump','BarackObama','HillaryClinton','GovRichardson','BernieSanders','MartinOMalley','LincolnChafee','JimWebbUSA','JohnKasich','tedcruz','marcorubio','JebBush','NJGovChristie','CarlyFiorina','RickSantorum'])
users=set(['BarackObama','HillaryClinton','GovRichardson','SenChrisDodd','JoeBiden','SenJohnMcCain','GovMikeHuckabee','MittRomney','rudygiulianiGOP','fredthompson','BarackObama','MittRomney','RepRonPaul','newtgingrich','RickSantorum','GovernorPerry','JonHuntsman','MicheleBachmann','THEHermanCain','TimPawlenty','realDonaldTrump','HillaryClinton','BernieSanders','MartinOMalley','LincolnChafee','JimWebbUSA','JohnKasich','tedcruz','marcorubio','JebBush','NJGovChristie','CarlyFiorina','RickSantorum','RandPaul','GovMikeHuckabee','GovernorPataki','LindseyGrahamSC','BobbyJindal','GovWalker','GovernorPerry'])
users=users-oldUsers

for user in users:
    try:
        print user
        ts.get_all_tweets(user,'tweets/'+user+'/')
    except:
        print 'ERROR FOR USER ' + user
        traceback.print_exc()
