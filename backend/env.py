import os

def isLocal():
    return os.getenv('GOOGLE_CLOUD_PROJECT') is None

def isProd():
    return not isLocal()