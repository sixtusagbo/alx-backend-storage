#!/usr/bin/env python3
"""Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """Update school topics"""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
