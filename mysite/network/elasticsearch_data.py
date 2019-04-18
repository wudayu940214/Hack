# encoding=utf-8

import json
from elasticsearch import Elasticsearch
import time


def queryES(keywords, name, period, index="twitter_data", doc_type="test_type", ip="148.70.167.220"):
    es = Elasticsearch(ip)
    if period == '':
        period = "01/01/2014 12:00 AM - 04/18/2019 11:59 PM"
    starttime_str = period.split(" - ")[0].replace("/", " ").strip()
    endtime_str = period.split(" - ")[1].replace("/", " ").strip()
    print("*" * 30)
    starttime = time.strftime("%Y-%m-%dT%H:%M", time.strptime(starttime_str, "%m %d %Y %I:%M %p"))
    endtime = time.strftime("%Y-%m-%dT%H:%M", time.strptime(endtime_str, "%m %d %Y %I:%M %p"))
    # result = starttime + ";" + endtime
    # starttime = result.split(';')[0]
    # endtime = result.split(';')[1]
    querywithname = {
        "query": {
            "bool": {
                "must": [
                    {'match': {'text': keywords}},
                    {'match': {'name': name}},
                    {"range": {"time": {"gte": starttime, "lt": endtime}}},
                ]
            }
        }
    }
    querywithoutname = {
        "query": {
            "bool": {
                "must": [
                    {'match': {'text': keywords}},
                    {"range": {"time": {"gte": starttime, "lt": endtime}}},
                ]
            }
        }
    }
    query = querywithname
    if name == '':
        query = querywithoutname
    # allDoc = es.search(index=index, doc_type=doc_type, body=query)
    allDoc = es.search(index=index, body=query)
    list = allDoc['hits']['hits']
    return list
    pass