import tweepy
auth = tweepy.OAuthHandler("WDCaTo70RKGCLzOuWzS5BG7Zg", "uhLx8zwIRB2cIgR2ImpYyoX1z4ohBBRe1QKG3R7kYKCdsp3uBH")
auth.set_access_token("840945467005534208-vkm8UnpBW1ENsrPF9HzBFHk5kxf8l3n", "PBYqMWRmTHQMCx3cKSMKnhhbiWsGuNx0tngwNZj4FhPYc")
api = tweepy.API(auth,wait_on_rate_limit=True)
key = api.search("Oracle",lang="en",count="100")
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'http://148.70.167.220'}])

for info in key:
    print info.text
    es.index(index="twitter_data",doc_type="test_type",id=info.id,body={"name":info.user.name,"text":info.text,"time":info.created_at,"retweet_count":info.retweet_count})
