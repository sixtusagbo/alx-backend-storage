#!/usr/bin/env python3
"""Search for schools by topic"""


def schools_by_topic(mongo_collection, topic):
    """Return the list of school having a specific topic"""
    return list(mongo_collection.find({'topics': topic}))
