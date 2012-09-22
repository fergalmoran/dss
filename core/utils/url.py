import urlparse

__author__ = 'fergalm'
def urlclean(url):
    #remove double slashes
    ret = urlparse.urlparse(url).path.replace('//', '/')
    return ret