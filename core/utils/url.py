import urlparse

__author__ = 'fergalm'
def urlclean(url):
    #remove double slashes
    ret = urlparse.urljoin(url, urlparse.urlparse(url).path.replace('//','/'))
    return ret