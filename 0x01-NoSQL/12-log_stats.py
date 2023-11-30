#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def count_docs(collection) -> int:
    """Return the number of documents in a collection"""
    return collection.count_documents({})


def find_count(collection, key: str, value: str) -> int:
    """Return the number of documents that match the search"""
    return collection.count_documents({key: value})


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
