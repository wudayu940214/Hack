import tweepy
auth = tweepy.OAuthHandler("WDCaTo70RKGCLzOuWzS5BG7Zg", "uhLx8zwIRB2cIgR2ImpYyoX1z4ohBBRe1QKG3R7kYKCdsp3uBH")
auth.set_access_token("840945467005534208-vkm8UnpBW1ENsrPF9HzBFHk5kxf8l3n", "PBYqMWRmTHQMCx3cKSMKnhhbiWsGuNx0tngwNZj4FhPYc")
api = tweepy.API(auth,wait_on_rate_limit=True,proxy="socks5://127.0.0.1:1080")
user = api.friends_ids("zhengyu214")
from elasticsearch import Elasticsearch
es = Elasticsearch()
#user = api.followers()
for tweet in user:
        newtweet = api.friends_ids(str(tweet))
        #p.write(str(tweet)+"\n")
        for tw in newtweet:
            #print tw
            #p.write(str(tw)+"\n")
            #person.append(str(tweet.id))
            #p.write(str(tweet.id)+"\n")
    #print str(tweet.id)
            Info = api.user_timeline(str(tw))
            try:
                for info in Info:
                #print info
                    es.index(index="twitter_data",doc_type="test_type",id=info.id,body={"name":info.user.name,"text":info.text,"time":info.created_at,"retweet_count":info.retweet_count})
                
                #p.write(info.text.encode('utf-8')+"\n")
            except tweepy.TweepError:
                continue
        #print info
    #print tweet
# for per in person:
#     follower = api.followers(per)
#     for tweet in follower:
#         person.append(str(tweet.id))
#         p.write(str(tweet.id)+"\n")
#Info = api.user_timeline(str(tw))
#for info in Info:
                #print info.text
    #p.write(info.text.encode('utf-8')+"\n")

# fo = open("example.txt", "w")
# for num in range(0,100):
#     public_tweets = api.statuses_lookup()
#     for tweet in public_tweets:
#         print tweet.text
#         fo.write(tweet.text.encode('utf-8')+"\n")
# fo.close()