__author__ = 'fergalm'
def urlclean(url):
    ret = url.replace('//', '/')
    return ret