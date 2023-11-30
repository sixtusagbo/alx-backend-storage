#!/usr/bin/env python3
"""Log stats - new version"""
from pymongo import MongoClient


def count_docs(collection) -> int:
    """Return the number of documents in a collection"""
    return collection.count_documents({})


def find_count(collection, key: str, value: str) -> int:
    """Return the number of documents that match the search"""
    return collection.count_documents({key: value})


def ips_by_count(collection) -> list:
    """Return the list of dict of ips and their count"""
    pipeline = [
        {
            "$project": {"_id": 0, "ip": 1},
        },
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1},
            },
        },
        {
            "$sort": {
                "count": -1,
            },
        },
        {
            "$limit": 10,
        },
    ]
    return collection.aggregate(pipeline)


if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    collection = client.logs.nginx
    print("{} logs".format(count_docs(collection)))
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        print(
            "\tmethod {}: {}".format(
                method, find_count(collection, "method", method)
            )
        )
    print("{} status check".format(find_count(collection, "path", "/status")))
    print("IPs:")
    top_ten_ips = ips_by_count(collection)
    for ip in top_ten_ips:
        print("\t{}: {}".format(ip.get("_id"), ip.get("count")))
