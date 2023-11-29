#!/usr/bin/env python3
"""Insert a document in Python"""

def insert_school(mongo_collection, **kwargs):
    """Return newly inserted document's _id"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
